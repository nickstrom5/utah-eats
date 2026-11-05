import SwiftUI
import UIKit
import CoreText

/// Utah palette from the 2024 state flag (provisional, 2026-11-05; Nick decides, playbook/05-naming.md), light only. Loyalties split the
/// state (Utes red, BYU blue, Utah State), so the flag's navy and dark red are balanced and neither reads as a school: flag navy #071D49
/// (16.4:1 on white) for titles, tint and accents; flag red #AA0200 (white on it 7.7:1) for the hand-checked guide cards under white
/// text and chips; flag amber #FFB81D only as a pin and card fill under navy text (as text on white it's 1.7:1); a snow-white #FAF7F0
/// page. The names `green`/`gold` are kept from Wisconsin Eats so the shared views read the same; here `green` is flag navy and `gold`
/// is flag red.
enum Theme {
    static let green = Color(hex: 0x071D49)      // flag navy: titles, tint, primary text accents
    static let green2 = Color(hex: 0x1F3A6B)
    static let gold = Color(hex: 0xAA0200)       // flag red: card fills under white text, chips
    static let goldSoft = Color(hex: 0xF6D8D4)   // soft red
    static let lime = Color(hex: 0xFFB81D)       // flag amber, fills only (hand-checked pins, the title shadow), under navy text
    static let limeSoft = Color(hex: 0xFFEDC4)
    static let sand = Color(hex: 0xFAF7F0)       // the Home background, snow white
    static let red = Color(hex: 0xAA0200)        // honors chips
    static let sandstone = Color(hex: 0xB5451B)  // red-rock accent (5.5:1 on white)
    static let teal = Color(hex: 0x1F6E78)       // Great Salt Lake accent (5.9:1 on white)
    static let ink = Color(hex: 0x14181F)
    static let ink2 = Color(hex: 0x2E3440)
    static let muted = Color(hex: 0x5B6270)
    static let surface = Color.white
    static let surface2 = Color(hex: 0xF1EEE6)
    static let surface3 = Color(hex: 0xE4DFD3)
    static let rule = Color(hex: 0xE4DFD3)
    static let rule2 = Color(hex: 0xCCC4B3)
}

extension Color {
    init(hex: UInt32) {
        self.init(red: Double((hex >> 16) & 0xFF) / 255, green: Double((hex >> 8) & 0xFF) / 255, blue: Double(hex & 0xFF) / 255)
    }
}

/// A small uppercase label: "STONE CRAB", "1 MICHELIN STAR".
struct Chip: View {
    enum Style { case gold, green, red, plain, dashed }
    let text: String
    var style: Style = .plain

    var body: some View {
        Text(text.uppercased())
            .font(.caption2.weight(.bold))
            .tracking(0.4)
            .padding(.horizontal, 7).padding(.vertical, 3)
            .foregroundStyle(style == .green || style == .red ? Color.white : style == .dashed ? Theme.muted : style == .gold ? Theme.ink : Theme.green)
            .background {
                RoundedRectangle(cornerRadius: 5).fill(style == .gold ? Theme.goldSoft : style == .green ? Theme.green : style == .red ? Theme.red
                                                       : style == .dashed ? .clear : Theme.surface2)
            }
            .overlay {
                if style == .dashed { RoundedRectangle(cornerRadius: 5).strokeBorder(Theme.rule2, style: StrokeStyle(lineWidth: 1, dash: [3, 2])) }
            }
            .accessibilityLabel(text)
    }
}

/// Beehive Eats' lettering: the system face drawn compressed and heavy for titles and guide names (like a show poster), and the
/// system monospaced face for numbers, dates and small labels. No bundled fonts.
struct DisplayFont: ViewModifier {
    let size: CGFloat
    var weight: Font.Weight = .black
    @ScaledMetric(relativeTo: .body) private var scale: CGFloat = 1

    func body(content: Content) -> some View {
        content.font(.system(size: size * min(scale, 1.6), weight: weight).width(.compressed))
    }
}

/// Numbers, dates and small labels in the system monospaced face, scaled like DisplayFont.
struct MonoFont: ViewModifier {
    let size: CGFloat
    var weight: Font.Weight = .semibold
    @ScaledMetric(relativeTo: .body) private var scale: CGFloat = 1

    func body(content: Content) -> some View {
        content.font(.system(size: size * min(scale, 1.6), weight: weight, design: .monospaced))
    }
}

extension View {
    func displayFont(_ size: CGFloat, weight: Font.Weight = .black) -> some View {
        modifier(DisplayFont(size: size, weight: weight))
    }

    func monoFont(_ size: CGFloat, weight: Font.Weight = .semibold) -> some View {
        modifier(MonoFont(size: size, weight: weight))
    }
}

/// The header band: a five-peak Wasatch skyline in flag navy (the 2024 flag's peaks) over a red-rock baseline, ending at the right in a
/// sandstone arch.
struct Stripes: View {
    var height: CGFloat = 6

    var body: some View {
        Canvas { ctx, size in
            let w = size.width, h = size.height, base = h * 0.78
            // five peaks across the first three quarters of the band, the middle one tallest
            let span = w * 0.78, step = span / 5
            var peaks = Path()
            peaks.move(to: CGPoint(x: 0, y: base))
            for (i, rise) in [0.55, 0.75, 1.0, 0.7, 0.5].enumerated() {
                let x0 = CGFloat(i) * step
                peaks.addLine(to: CGPoint(x: x0 + step / 2, y: base - base * rise))
                peaks.addLine(to: CGPoint(x: x0 + step, y: base))
            }
            peaks.addLine(to: CGPoint(x: 0, y: base))
            ctx.fill(peaks, with: .color(Theme.green))
            // the arch: a sandstone block with a round opening
            let ax = span + (w - span) * 0.35, aw = min((w - span) * 0.5, base * 1.6)
            ctx.fill(Path(CGRect(x: ax, y: base * 0.25, width: aw, height: base * 0.75)), with: .color(Theme.sandstone))
            ctx.fill(Path(ellipseIn: CGRect(x: ax + aw * 0.22, y: base * 0.5, width: aw * 0.56, height: base)), with: .color(Theme.sand))
            // the red-rock baseline last, so the arch's opening stands on it
            ctx.fill(Path(CGRect(x: 0, y: base, width: w, height: h - base)), with: .color(Theme.gold))
        }
        .frame(height: height * 2.4)
        .clipShape(RoundedRectangle(cornerRadius: 3))
        .accessibilityHidden(true)
    }
}

extension View {
    /// An inline navigation title in the display type. UINavigationBar.appearance() didn't reach every SwiftUI bar on iOS 27
    /// (the Map title went from compressed blue to plain black after a push and pop; place titles were always plain), so the
    /// title is our own view in the bar. The navigation title is still set, for the back button and VoiceOver.
    func inlineTitle(_ title: String) -> some View {
        navigationTitle(title)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .principal) {
                    Text(title).displayFont(19, weight: .heavy).foregroundStyle(Theme.green)
                        .lineLimit(1).minimumScaleFactor(0.7)
                        .accessibilityAddTraits(.isHeader)
                }
            }
    }
}
