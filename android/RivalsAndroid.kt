package com.kercx.rivals

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationManager
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.button.MaterialButton
import com.google.android.material.progressindicator.CircularProgressIndicator
import com.google.android.material.textfield.TextInputEditText
import kotlinx.coroutines.*
import org.json.JSONObject
import java.net.URL

class MainActivity : AppCompatActivity() {
    
    private lateinit var usernameInput: TextInputEditText
    private lateinit var scanButton: MaterialButton
    private lateinit var progressBar: CircularProgressIndicator
    private lateinit var resultsRecyclerView: RecyclerView
    private lateinit var resultAdapter: ResultAdapter
    
    private val results = mutableListOf<PlatformResult>()
    private val scanner = RivalsScanner()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        initViews()
        setupRecyclerView()
        setupListeners()
        checkPermissions()
    }
    
    private fun initViews() {
        usernameInput = findViewById(R.id.usernameInput)
        scanButton = findViewById(R.id.scanButton)
        progressBar = findViewById(R.id.progressBar)
        resultsRecyclerView = findViewById(R.id.resultsRecyclerView)
    }
    
    private fun setupRecyclerView() {
        resultAdapter = ResultAdapter(results)
        resultsRecyclerView.layoutManager = LinearLayoutManager(this)
        resultsRecyclerView.adapter = resultAdapter
    }
    
    private fun setupListeners() {
        scanButton.setOnClickListener {
            val username = usernameInput.text.toString().trim()
            if (username.isNotEmpty()) {
                startScan(username)
            } else {
                Toast.makeText(this, "Enter username", Toast.LENGTH_SHORT).show()
            }
        }
    }
    
    private fun startScan(username: String) {
        scanButton.isEnabled = false
        progressBar.visibility = android.view.View.VISIBLE
        results.clear()
        resultAdapter.notifyDataSetChanged()
        
        GlobalScope.launch(Dispatchers.IO) {
            val scanResults = scanner.scan(username)
            
            withContext(Dispatchers.Main) {
                results.addAll(scanResults)
                resultAdapter.notifyDataSetChanged()
                scanButton.isEnabled = true
                progressBar.visibility = android.view.View.GONE
                
                val foundCount = results.count { it.exists }
                Toast.makeText(
                    this@MainActivity,
                    "Scan complete! Found: $foundCount profiles",
                    Toast.LENGTH_LONG
                ).show()
            }
        }
    }
    
    private fun checkPermissions() {
        val permissions = arrayOf(
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_NETWORK_STATE
        )
        
        val missingPermissions = permissions.filter {
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }
        
        if (missingPermissions.isNotEmpty()) {
            ActivityCompat.requestPermissions(this, missingPermissions.toTypedArray(), 100)
        }
    }
}

// MARK: - Scanner Class
class RivalsScanner {
    
    private val platforms = listOf(
        Platform("GitHub", "https://github.com/%s"),
        Platform("Twitter", "https://twitter.com/%s"),
        Platform("Instagram", "https://instagram.com/%s"),
        Platform("Reddit", "https://reddit.com/user/%s"),
        Platform("LinkedIn", "https://linkedin.com/in/%s"),
        Platform("YouTube", "https://youtube.com/@%s"),
        Platform("TikTok", "https://tiktok.com/@%s"),
        Platform("Telegram", "https://t.me/%s")
    )
    
    suspend fun scan(username: String): List<PlatformResult> = coroutineScope {
        val jobs = platforms.map { platform ->
            async(Dispatchers.IO) {
                checkPlatform(platform, username)
            }
        }
        jobs.awaitAll()
    }
    
    private fun checkPlatform(platform: Platform, username: String): PlatformResult {
        val url = String.format(platform.url, username)
        val exists = try {
            val connection = URL(url).openConnection()
            connection.setRequestProperty("User-Agent", "Rivals-Mobile/1.0")
            connection.connect()
            val responseCode = (connection as java.net.HttpURLConnection).responseCode
            responseCode == 200
        } catch (e: Exception) {
            false
        }
        return PlatformResult(platform.name, url, exists)
    }
}

// MARK: - Data Models
data class Platform(val name: String, val url: String)
data class PlatformResult(val name: String, val url: String, val exists: Boolean)

// MARK: - RecyclerView Adapter
class ResultAdapter(private val results: List<PlatformResult>) : 
    RecyclerView.Adapter<ResultAdapter.ViewHolder>() {
    
    class ViewHolder(itemView: android.view.View) : RecyclerView.ViewHolder(itemView) {
        val platformName: TextView = itemView.findViewById(R.id.platformName)
        val platformUrl: TextView = itemView.findViewById(R.id.platformUrl)
        val statusIcon: ImageView = itemView.findViewById(R.id.statusIcon)
    }
    
    override fun onCreateViewHolder(parent: android.view.ViewGroup, viewType: Int): ViewHolder {
        val view = android.view.LayoutInflater.from(parent.context)
            .inflate(R.layout.item_result, parent, false)
        return ViewHolder(view)
    }
    
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val result = results[position]
        holder.platformName.text = result.name
        holder.platformUrl.text = result.url
        holder.statusIcon.setImageResource(
            if (result.exists) android.R.drawable.checkbox_on_background
            else android.R.drawable.checkbox_off_background
        )
    }
    
    override fun getItemCount() = results.size
}

// MARK: - Mobile Device Fingerprinting
class DeviceFingerprinter(private val context: Context) {
    
    fun getDeviceInfo(): JSONObject {
        return JSONObject().apply {
            put("manufacturer", android.os.Build.MANUFACTURER)
            put("model", android.os.Build.MODEL)
            put("android_version", android.os.Build.VERSION.RELEASE)
            put("sdk_version", android.os.Build.VERSION.SDK_INT)
            put("device_id", getDeviceId())
        }
    }
    
    private fun getDeviceId(): String {
        // This would use Android ID, Advertising ID, etc.
        return android.provider.Settings.Secure.getString(
            context.contentResolver,
            android.provider.Settings.Secure.ANDROID_ID
        ) ?: "unknown"
    }
    
    fun getLocation(): Location? {
        val locationManager = context.getSystemService(Context.LOCATION_SERVICE) as LocationManager
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) 
            == PackageManager.PERMISSION_GRANTED) {
            return locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER)
        }
        return null
    }
    
    fun getNetworkInfo(): JSONObject {
        return JSONObject().apply {
            put("wifi_enabled", isWifiEnabled())
            put("cellular_type", getCellularType())
        }
    }
    
    private fun isWifiEnabled(): Boolean {
        val wifiManager = context.getSystemService(Context.WIFI_SERVICE) as android.net.wifi.WifiManager
        return wifiManager.isWifiEnabled
    }
    
    private fun getCellularType(): String {
        // Returns: "4G", "5G", "LTE", etc.
        val telephonyManager = context.getSystemService(Context.TELEPHONY_SERVICE) as android.telephony.TelephonyManager
        return when (telephonyManager.networkType) {
            android.telephony.TelephonyManager.NETWORK_TYPE_LTE -> "4G/LTE"
            android.telephony.TelephonyManager.NETWORK_TYPE_NR -> "5G"
            else -> "Unknown"
        }
    }
}
