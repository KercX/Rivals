//
//  RivalsiOS.swift
//  Rivals - Mobile OSINT Scanner
//  Created by KercX
//

import SwiftUI
import Network
import CoreLocation

// MARK: - Main App Structure
@main
struct RivalsApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

// MARK: - Main Content View
struct ContentView: View {
    @State private var username: String = ""
    @State private var results: [PlatformResult] = []
    @State private var isScanning: Bool = false
    @State private var showingResults: Bool = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Header
                VStack {
                    Image(systemName: "magnifyingglass.circle.fill")
                        .font(.system(size: 70))
                        .foregroundColor(.blue)
                    Text("Rivals OSINT")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                    Text("Mobile Intelligence Platform")
                        .font(.subheadline)
                        .foregroundColor(.gray)
                }
                .padding(.top, 40)
                
                // Input Field
                VStack(alignment: .leading) {
                    Text("Target Username")
                        .font(.headline)
                    TextField("Enter username", text: $username)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .autocapitalization(.none)
                        .disableAutocorrection(true)
                }
                .padding(.horizontal)
                
                // Scan Button
                Button(action: startScan) {
                    HStack {
                        if isScanning {
                            ProgressView()
                                .progressViewStyle(CircularProgressViewStyle(tint: .white))
                        } else {
                            Image(systemName: "play.circle.fill")
                        }
                        Text(isScanning ? "Scanning..." : "Start Scan")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(username.isEmpty || isScanning ? Color.gray : Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
                .disabled(username.isEmpty || isScanning)
                .padding(.horizontal)
                
                // Quick Actions
                HStack(spacing: 15) {
                    QuickActionButton(title: "Test User", action: { username = "johndoe" })
                    QuickActionButton(title: "Clear", action: { username = "" })
                    QuickActionButton(title: "Example", action: { username = "kercx" })
                }
                .padding(.horizontal)
                
                Spacer()
                
                // Results Summary
                if showingResults && !results.isEmpty {
                    ResultsSummaryView(results: results)
                        .padding()
                }
            }
            .navigationBarTitleDisplayMode(.inline)
            .sheet(isPresented: $showingResults) {
                ResultsDetailView(results: results)
            }
        }
    }
    
    func startScan() {
        isScanning = true
        showingResults = false
        
        // Simulate OSINT scan (replace with actual API call)
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            results = [
                PlatformResult(name: "GitHub", url: "https://github.com/\(username)", exists: true),
                PlatformResult(name: "Twitter", url: "https://twitter.com/\(username)", exists: true),
                PlatformResult(name: "Instagram", url: "https://instagram.com/\(username)", exists: false),
                PlatformResult(name: "Reddit", url: "https://reddit.com/user/\(username)", exists: true)
            ]
            isScanning = false
            showingResults = true
        }
        
        // Real implementation would call backend API:
        // RivalsAPI.shared.scan(username: username) { result in
        //     self.results = result
        //     self.isScanning = false
        //     self.showingResults = true
        // }
    }
}

// MARK: - Quick Action Button
struct QuickActionButton: View {
    let title: String
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.caption)
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(Color(.systemGray5))
                .cornerRadius(8)
        }
    }
}

// MARK: - Data Models
struct PlatformResult: Identifiable, Codable {
    let id = UUID()
    let name: String
    let url: String
    let exists: Bool
}

// MARK: - Results Summary View
struct ResultsSummaryView: View {
    let results: [PlatformResult]
    
    var foundCount: Int {
        results.filter { $0.exists }.count
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Scan Complete")
                .font(.headline)
            HStack {
                Text("Found:")
                    .foregroundColor(.green)
                Text("\(foundCount)")
                    .fontWeight(.bold)
                Text("Not Found:")
                    .foregroundColor(.red)
                Text("\(results.count - foundCount)")
                    .fontWeight(.bold)
            }
            .font(.subheadline)
            
            Button("View Details") {
                // Action handled by parent
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
}

// MARK: - Results Detail View
struct ResultsDetailView: View {
    let results: [PlatformResult]
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationView {
            List(results) { result in
                HStack {
                    Image(systemName: result.exists ? "checkmark.circle.fill" : "xmark.circle.fill")
                        .foregroundColor(result.exists ? .green : .red)
                    VStack(alignment: .leading) {
                        Text(result.name)
                            .font(.headline)
                        Text(result.url)
                            .font(.caption)
                            .foregroundColor(.blue)
                    }
                }
                .padding(.vertical, 4)
            }
            .navigationTitle("Scan Results")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
}

// MARK: - API Service (Concept)
class RivalsAPI {
    static let shared = RivalsAPI()
    private let baseURL = "https://api.rivals.osint/v1"
    
    func scan(username: String, completion: @escaping ([PlatformResult]) -> Void) {
        guard let url = URL(string: "\(baseURL)/scan/\(username)") else {
            completion([])
            return
        }
        
        URLSession.shared.dataTask(with: url) { data, _, error in
            guard let data = data, error == nil else {
                completion([])
                return
            }
            
            let results = try? JSONDecoder().decode([PlatformResult].self, from: data)
            DispatchQueue.main.async {
                completion(results ?? [])
            }
        }.resume()
    }
}

// MARK: - Location Permissions for OSINT
class LocationManager: NSObject, CLLocationManagerDelegate {
    private let manager = CLLocationManager()
    
    override init() {
        super.init()
        manager.delegate = self
    }
    
    func requestPermission() {
        manager.requestWhenInUseAuthorization()
    }
    
    func getCurrentLocation() -> CLLocation? {
        return manager.location
    }
}

// MARK: - Preview
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
