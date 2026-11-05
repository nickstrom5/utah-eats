// Beehive Eats brand (provisional, 2026-11-05; Nick picks the name, icon and palette): the app icon is concept A of
// scripts/icon-concepts.swift, fries in a red carton with a cup of pink fry sauce, on the 2024 flag's navy; the shared Eats Ranked
// icon style, state-prompts/ICON-STYLE.md, no backing shape. No state seal, no beehive emblem, no team marks.
// Usage, from ut-eats/: swift scripts/make-brand.swift   -> UtahEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png,
// docs/ favicons and touch icons, docs/og.png. scripts/make-site.py draws the same mark as its inline SVG: change both together.
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let NAVY: UInt32 = 0x071D49, RED: UInt32 = 0xAA0200, AMBER: UInt32 = 0xFFB81D, PINK: UInt32 = 0xEE8C78, WHITE: UInt32 = 0xF7F3EA
let SANDSTONE: UInt32 = 0xB5451B, SNOW: UInt32 = 0xFAF7F0

/// Fries and fry sauce. CoreGraphics y-up, s = canvas size. Identical to icon-concepts.swift's concept A.
func fries(_ c: CGContext, _ s: CGFloat) {
    func P(_ x: CGFloat, _ y: CGFloat) -> CGPoint { CGPoint(x: x * s, y: y * s) }
    // the fries: seven amber sticks standing out of the carton, uneven tops
    c.setFillColor(rgb(AMBER))
    for (i, top) in [0.77, 0.83, 0.80, 0.86, 0.81, 0.85, 0.76].enumerated() {
        let x = 0.205 + CGFloat(i) * 0.054
        c.fill(CGRect(x: x * s, y: 0.46 * s, width: 0.046 * s, height: (CGFloat(top) - 0.46) * s))
    }
    // the carton: a red trapezoid, wider at the top
    let box = CGMutablePath()
    box.move(to: P(0.17, 0.58)); box.addLine(to: P(0.63, 0.58)); box.addLine(to: P(0.585, 0.24)); box.addLine(to: P(0.215, 0.24)); box.closeSubpath()
    c.setFillColor(rgb(RED)); c.addPath(box); c.fillPath()
    // the fry sauce: a white cup, the pink sauce showing at its rim
    c.setFillColor(rgb(WHITE)); c.fill(CGRect(x: 0.62 * s, y: 0.22 * s, width: 0.21 * s, height: 0.14 * s))
    c.fillEllipse(in: CGRect(x: 0.62 * s, y: 0.17 * s, width: 0.21 * s, height: 0.11 * s))
    c.setFillColor(rgb(PINK)); c.fillEllipse(in: CGRect(x: 0.62 * s, y: 0.30 * s, width: 0.21 * s, height: 0.11 * s))
}


func render(_ n: Int, _ path: String, background: Bool) {
    let ctx = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: background ? CGImageAlphaInfo.noneSkipLast.rawValue : CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.setShouldAntialias(true)
    if background { ctx.setFillColor(rgb(NAVY)); ctx.fill(CGRect(x: 0, y: 0, width: n, height: n)) }
    fries(ctx, CGFloat(n))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
render(1024, "UtahEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png", background: true)
try? FileManager.default.createDirectory(atPath: "docs", withIntermediateDirectories: true)
for (n, name) in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png"), (32, "favicon-32.png")] {
    render(n, "docs/" + name, background: true)
}

/// The share image (1200 x 630): flag navy, the fries at the left, the name and tagline at the right, and the app's header band
/// along the bottom: five Wasatch peaks in navy-blue over a red-rock baseline, ending in a sandstone arch, on snow white.
func og(_ path: String) {
    let W = 1200, H = 630
    let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true)
    ctx.setFillColor(rgb(NAVY)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
    // the band (y-up): snow ground, five peaks, the arch, the red-rock baseline
    let band: CGFloat = 70, base: CGFloat = 14
    ctx.setFillColor(rgb(SNOW)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: Int(band)))
    let span = CGFloat(W) * 0.78, step = span / 5
    let peaks = CGMutablePath(); peaks.move(to: CGPoint(x: 0, y: base))
    for (i, rise) in [0.55, 0.75, 1.0, 0.7, 0.5].enumerated() {
        let x0 = CGFloat(i) * step
        peaks.addLine(to: CGPoint(x: x0 + step / 2, y: base + (band - base) * CGFloat(rise))); peaks.addLine(to: CGPoint(x: x0 + step, y: base))
    }
    peaks.closeSubpath(); ctx.setFillColor(rgb(0x1F3A6B)); ctx.addPath(peaks); ctx.fillPath()
    let ax = span + (CGFloat(W) - span) * 0.3, aw: CGFloat = 120
    ctx.setFillColor(rgb(SANDSTONE)); ctx.fill(CGRect(x: ax, y: base, width: aw, height: band * 0.72))
    ctx.setFillColor(rgb(SNOW)); ctx.fillEllipse(in: CGRect(x: ax + aw * 0.22, y: base - band * 0.45, width: aw * 0.56, height: band * 0.9))
    ctx.setFillColor(rgb(RED)); ctx.fill(CGRect(x: 0, y: 0, width: CGFloat(W), height: base))
    ctx.saveGState(); ctx.translateBy(x: 40, y: 90); fries(ctx, 500); ctx.restoreGState()
    let ns = NSGraphicsContext(cgContext: ctx, flipped: false)
    NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current = ns
    let title = NSFont(name: "AvenirNextCondensed-Heavy", size: 96) ?? NSFont.boldSystemFont(ofSize: 84)
    let sub = NSFont(name: "AvenirNextCondensed-DemiBold", size: 38) ?? NSFont.boldSystemFont(ofSize: 34)
    NSAttributedString(string: "BEEHIVE EATS", attributes: [.font: title, .foregroundColor: NSColor.white]).draw(at: NSPoint(x: 580, y: 340))
    NSAttributedString(string: "PASTRAMI BURGERS, PIE & RED ROCK", attributes: [.font: sub, .foregroundColor: NSColor(srgbRed: 1.0, green: 0.722, blue: 0.114, alpha: 1)]).draw(at: NSPoint(x: 584, y: 282))
    NSGraphicsContext.restoreGraphicsState()
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
og("docs/og.png")
