import Foundation
import CoreLocation
import UIKit

/// `-screenshot <name>` opens one screen with fixed state for App Store screenshots (scripts/capture-screenshots.sh).
/// Names: home, classics, redrock, burgers, islands, skitowns, pies, honors, oldest, detail, map, saved, about.
enum ScreenshotMode {
    /// Debug builds only: an App Store build ignores the launch argument, so no one can reach seeded screens or fake locations.
    static var name: String? {
        #if DEBUG
        let args = ProcessInfo.processInfo.arguments
        guard let i = args.firstIndex(of: "-screenshot"), i + 1 < args.count else { return nil }
        return args[i + 1]
        #else
        return nil
        #endif
    }
    static var isActive: Bool { name != nil }

    @MainActor
    static func apply(to model: AppModel) {
        guard let name, model.isLoaded else { return }
        model.filters = Filters()
        // downtown Salt Lake City (Temple Square), so "nearest" lists have distances without a permission prompt
        model.screenshotLocation = CLLocation(latitude: 40.7700, longitude: -111.8920)
        // by name and town, ignoring case, so a rebuild with a slightly different casing still finds the place; the hand-checked one first
        let pick = { (n: String, town: String?) -> Place? in
            let hits = model.places.filter { $0.name.caseInsensitiveCompare(n) == .orderedSame && (town == nil || $0.city == town) }
            return hits.first(where: \.handChecked) ?? hits.first
        }
        for p in [pick("Ruth's Diner", "Salt Lake City"), pick("Hell's Backbone Grill & Farm", "Boulder"), pick("Red Iguana", "Salt Lake City")]
            .compactMap({ $0 }) where !model.isSaved(p) {
            model.toggleSaved(p)
        }
        let open = { (g: Guide) in model.tab = .guides; model.selectedGuide = g; model.guidesPath = [.guide(g)] }
        switch name {
        case "classics": open(.classics)
        case "redrock":
            // Torrey, at Capitol Reef, between Boulder's and Moab's stops
            model.screenshotLocation = CLLocation(latitude: 38.2997, longitude: -111.4199)
            open(.redRock)
        case "burgers": open(.burgers)
        case "islands": open(.islands)
        case "skitowns":
            // Park City's Main Street
            model.screenshotLocation = CLLocation(latitude: 40.6461, longitude: -111.4980)
            open(.skiTowns)
        case "pies":
            // Bryce Canyon City, on Scenic Byway 12
            model.screenshotLocation = CLLocation(latitude: 37.6740, longitude: -112.1570)
            open(.pies)
        case "honors": open(.honors)
        case "oldest": open(.oldest)
        case "detail":
            // Feldman's Deli: a Salt Lake classic and a MICHELIN Bib Gourmand, with its note
            open(.classics)
            if let p = pick("Feldman's Deli", "Salt Lake City") ?? model.places.first {
                model.selectedPlace = p; model.guidesPath.append(.place(p))
            }
        case "map": model.tab = .map
        case "saved": model.tab = .saved
        case "about": model.tab = .about
        default: model.tab = .guides; model.selectedGuide = nil
        }
        // iPad shows the place column next to every list, so give each shot a place instead of "Pick a place": a different
        // honored or hand-checked one per shot.
        guard UIDevice.current.userInterfaceIdiom == .pad, model.selectedPlace == nil else { return }
        let place: Place? = switch name {
        case "home": pick("Ruth's Diner", "Salt Lake City")
        case "classics": pick("Red Iguana", "Salt Lake City")
        case "redrock": pick("Hell's Backbone Grill & Farm", "Boulder")
        case "burgers": pick("Crown Burgers", "Salt Lake City")
        case "islands": pick("Pacific Seas Restaurant", "Salt Lake City")
        case "skitowns": pick("Handle", "Park City")
        case "pies": pick("Thunderbird Restaurant", "Mount Carmel")
        case "map": pick("Red Iguana", "Salt Lake City")
        case "honors": pick("Monte", "South Salt Lake")
        case "oldest": pick("Shooting Star Saloon", "Huntsville")
        case "saved": pick("Hell's Backbone Grill & Farm", "Boulder")
        case "about": nil
        default: pick("Feldman's Deli", "Salt Lake City")
        }
        model.selectedPlace = place
    }
}
