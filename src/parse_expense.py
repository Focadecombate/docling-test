import mdformat
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    AcceleratorDevice,
    AcceleratorOptions,
    PdfPipelineOptions,
    TableFormerMode,
    TableStructureOptions,
    TesseractOcrOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption

from clean_html import parse_html


def pdf_to_markdown(source: str):
    pipeline_options = PdfPipelineOptions(
        do_ocr=True,
        do_table_structure=True,
        table_structure_options=TableStructureOptions(
            do_cell_matching=True, mode=TableFormerMode.ACCURATE
        ),
        accelerator_options=AcceleratorOptions(device=AcceleratorDevice.CUDA),
        ocr_options=TesseractOcrOptions(),
    )
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    result = converter.convert(source)
    return mdformat.text(parse_html(result.document.export_to_html()))


if __name__ == "__main__":
    file_name = "fatura-1.pdf"
    new_file_name = f"./{file_name.replace('pdf', 'md')}"
    result = pdf_to_markdown(file_name)
    with open(new_file_name, "w+") as file:
        file.write(result)
