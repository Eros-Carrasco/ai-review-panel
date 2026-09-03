// Renders each page of a PDF to PNG and extracts its text with page markers.
// macOS only (uses PDFKit). Usage: swift render_pdf.swift <input.pdf> <output-dir>
// Writes: <output-dir>/page-01.png ... and <output-dir>/text.txt with "=== PAGE N ===" markers.
import Foundation
import PDFKit
import AppKit

let args = CommandLine.arguments
guard args.count == 3 else { print("usage: swift render_pdf.swift <input.pdf> <output-dir>"); exit(1) }
let url = URL(fileURLWithPath: args[1]); let outDir = args[2]
try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true)
guard let doc = PDFDocument(url: url) else { print("cannot open \(args[1])"); exit(1) }
var allText = ""
for i in 0..<doc.pageCount {
    guard let page = doc.page(at: i) else { continue }
    let bounds = page.bounds(for: .mediaBox)
    let scale: CGFloat = 2.0
    let size = NSSize(width: bounds.width*scale, height: bounds.height*scale)
    let img = NSImage(size: size)
    img.lockFocus()
    NSColor.white.setFill(); NSBezierPath(rect: NSRect(origin: .zero, size: size)).fill()
    let ctx = NSGraphicsContext.current!.cgContext
    ctx.scaleBy(x: scale, y: scale)
    page.draw(with: .mediaBox, to: ctx)
    img.unlockFocus()
    if let tiff = img.tiffRepresentation, let rep = NSBitmapImageRep(data: tiff),
       let png = rep.representation(using: .png, properties: [:]) {
        try? png.write(to: URL(fileURLWithPath: "\(outDir)/page-\(String(format: "%02d", i+1)).png"))
    }
    allText += "=== PAGE \(i+1) ===\n" + (page.string ?? "") + "\n"
}
try? allText.write(toFile: "\(outDir)/text.txt", atomically: true, encoding: .utf8)
print("pages:", doc.pageCount)
