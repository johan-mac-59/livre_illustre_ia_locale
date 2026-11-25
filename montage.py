"""Montage final : PDF de livre illustré (une illustration + son texte par page)."""
from xml.sax.saxutils import escape
from mise_en_page import esc

from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer


def filigraner(source, destination, texte="NON VALIDÉE"):
    """Copie une image avec un filigrane diagonal rouge translucide, pour signaler qu'elle
    n'a pas passé les contrôles. L'image d'origine n'est pas modifiée."""
    image = PILImage.open(source).convert("RGBA")
    try:
        police = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", image.width // 7)
    except OSError:
        police = ImageFont.load_default()
    bloc = PILImage.new("RGBA", (image.width * 2, image.height // 3), (0, 0, 0, 0))
    ImageDraw.Draw(bloc).text((bloc.width // 2, bloc.height // 2), texte, font=police,
                              fill=(200, 0, 0, 130), anchor="mm", stroke_width=4,
                              stroke_fill=(255, 255, 255, 130))
    bloc = bloc.rotate(30, expand=True, resample=PILImage.BICUBIC)
    calque = PILImage.new("RGBA", image.size, (0, 0, 0, 0))
    calque.paste(bloc, ((image.width - bloc.width) // 2, (image.height - bloc.height) // 2), bloc)
    PILImage.alpha_composite(image, calque).convert("RGB").save(destination)
    return destination


def assembler_pdf(chemin_pdf, titre, scenes, images, legendes):
    """Écrit le PDF. scenes, images et legendes sont des listes de même longueur."""
    marge = 15 * mm
    largeur = A5[0] - 2 * marge
    style_titre = ParagraphStyle("titre", fontName="Times-Bold", fontSize=26, leading=32, alignment=1)
    style_corps = ParagraphStyle("corps", fontName="Times-Roman", fontSize=11.5, leading=16,
                                 spaceAfter=6)
    style_legende = ParagraphStyle("legende", fontName="Times-Italic", fontSize=10, leading=13,
                                   alignment=1, spaceAfter=8)
    doc = SimpleDocTemplate(str(chemin_pdf), pagesize=A5, title=titre, author="",
                            leftMargin=marge, rightMargin=marge, topMargin=marge, bottomMargin=marge)
    flux = [Spacer(1, 55 * mm), Paragraph(esc(titre), style_titre), PageBreak()]
    for i, (scene, image, legende) in enumerate(zip(scenes, images, legendes)):
        flux.append(Image(str(image), width=largeur, height=largeur))
        flux.append(Spacer(1, 3 * mm))
        if legende:
            flux.append(Paragraph(esc(legende), style_legende))
        for paragraphe in scene.split("\n\n"):
            flux.append(Paragraph(esc(" ".join(paragraphe.split())), style_corps))
        if i < len(scenes) - 1:
            flux.append(PageBreak())
    doc.build(flux)
    return chemin_pdf
