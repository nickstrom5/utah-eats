// Beehive Eats icon concepts (2026-11-05), drawn in the shared Eats Ranked style (state-prompts/ICON-STYLE.md): one flat, level,
// centred food on flag navy #071D49, no backing shape, no text or texture. Food hexes from the 2024 flag and the prompt's ideas:
// flag red #AA0200, flag amber #FFB81D, fry-sauce pink #EE8C78, a warm white #F7F3EA, scone brown #C9822F, lime #7DB343.
//   A  fries in a red carton with a cup of pink fry sauce beside it, front view
//   B  a puffy Utah scone with a pat of honey butter and a honey drizzle, front view
//   C  a dirty soda: a white cup of cola with a red straw and a lime wedge on the rim, front view
// Usage, from ut-eats/: swift scripts/icon-concepts.swift <out dir>   -> concept-{a,b,c}-1024.png
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let NAVY: UInt32 = 0x071D49, RED: UInt32 = 0xAA0200, AMBER: UInt32 = 0xFFB81D, PINK: UInt32 = 0xEE8C78, WHITE: UInt32 = 0xF7F3EA
let BROWN: UInt32 = 0xC9822F, LIME: UInt32 = 0x7DB343, COLA: UInt32 = 0x5A2E17

/// A: fries and fry sauce. CoreGraphics y-up, s = canvas size. Identical to make-brand.swift's fries().
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

/// B: a Utah scone: a puffy golden-brown round, a pale pat of honey butter, an amber drizzle down its front.
func scone(_ c: CGContext, _ s: CGFloat) {
    c.setFillColor(rgb(BROWN)); c.fillEllipse(in: CGRect(x: 0.14 * s, y: 0.26 * s, width: 0.72 * s, height: 0.42 * s))
    c.setFillColor(rgb(AMBER))
    c.fillEllipse(in: CGRect(x: 0.30 * s, y: 0.47 * s, width: 0.40 * s, height: 0.15 * s))
    c.fill(CGRect(x: 0.36 * s, y: 0.34 * s, width: 0.05 * s, height: 0.20 * s))
    c.fill(CGRect(x: 0.56 * s, y: 0.38 * s, width: 0.05 * s, height: 0.16 * s))
    c.setFillColor(rgb(WHITE)); c.fill(CGRect(x: 0.42 * s, y: 0.56 * s, width: 0.16 * s, height: 0.09 * s))
}

/// C: a dirty soda: a white cup, cola showing at the rim, a red straw, a lime wedge.
func soda(_ c: CGContext, _ s: CGFloat) {
    func P(_ x: CGFloat, _ y: CGFloat) -> CGPoint { CGPoint(x: x * s, y: y * s) }
    c.setFillColor(rgb(RED)); c.fill(CGRect(x: 0.57 * s, y: 0.60 * s, width: 0.05 * s, height: 0.28 * s))
    let cup = CGMutablePath()
    cup.move(to: P(0.30, 0.68)); cup.addLine(to: P(0.76, 0.68)); cup.addLine(to: P(0.69, 0.18)); cup.addLine(to: P(0.37, 0.18)); cup.closeSubpath()
    c.setFillColor(rgb(WHITE)); c.addPath(cup); c.fillPath()
    c.setFillColor(rgb(COLA)); c.fill(CGRect(x: 0.33 * s, y: 0.56 * s, width: 0.40 * s, height: 0.08 * s))
    c.setFillColor(rgb(LIME)); c.fillEllipse(in: CGRect(x: 0.23 * s, y: 0.60 * s, width: 0.17 * s, height: 0.17 * s))
}

func render(_ n: Int, _ path: String, _ draw: (CGContext, CGFloat) -> Void) {
    let ctx = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true)
    ctx.setFillColor(rgb(NAVY)); ctx.fill(CGRect(x: 0, y: 0, width: n, height: n))
    draw(ctx, CGFloat(n))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
let out = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "playbook/brand"
render(1024, out + "/concept-a-1024.png", fries)
render(1024, out + "/concept-b-1024.png", scone)
render(1024, out + "/concept-c-1024.png", soda)
