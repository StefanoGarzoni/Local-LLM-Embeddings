#Attention to the correct paths in the code below.
import fitz 
import io
from PIL import Image
import pytesseract
import os
import glob
import shutil

output_folder = 'path to the folder where the images will be extracted'
txt_folder='path to the folder where the txt files will be saved'
folder_path = 'path to the folder containing the pdf files' 

def clear_folder():
    folder_path = 'path to the folder where the images will be extracted'  
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path) 
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path) 
        except Exception as e:
            print(e)

def extract_elements_order_from_page(page):
    text_instances = []
    for text_block in page.get_text("dict")["blocks"]:
        if "lines" in text_block:
            for line in text_block["lines"]:
                for span in line["spans"]:
                    text_instances.append({
                        "type": "text",
                        "bbox": span["bbox"],  
                        "text": span["text"]
                    })

    image_instances = []
    for img in page.get_images(full=True):
        image_bbox = fitz.Rect(img[1:5])
        image_instances.append({
            "type": "image",
            "bbox": image_bbox
        })

    elements = text_instances + image_instances
    elements.sort(key=lambda e: e["bbox"][1])

    ordered_elements = []
    for element in elements:
        if element["type"] == "text":
            ordered_elements.append(tuple(element["bbox"]))
        elif element["type"] == "image":
            ordered_elements.append("image")

    return ordered_elements

def extract_elements_order_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    all_pages_elements = []
    
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        elements_order = extract_elements_order_from_page(page)
        all_pages_elements.append(elements_order)
    
    return all_pages_elements

def create_pagetxt(pdf_path,all_pages_elements):
    document = fitz.open(pdf_path)
    txtDoc=""
    for page_num, elements in enumerate(all_pages_elements):
        img_index=1
        if "image" in elements:
            for i in elements:
                if i=="image":
                    text=extract_text_from_image(f"Support folder path for temporary image saving{page_num+1}_{img_index}.jpeg")
                    img_index+=1
                else:
                    page = document.load_page(page_num)
                    text = page.get_text("text", clip=fitz.Rect(i))
                txtDoc+= text
        else:
            page = document.load_page(page_num)
            text = page.get_text()
            txtDoc+= text

    return txtDoc

def extract_text_from_image(image_path):

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)
    return text

def extract_images_from_pdf(pdf_path, output_folder):
    document = fitz.open(pdf_path)
    
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = document.extract_image(xref)
            image_bytes = base_image["image"]

            image_ext= "jpeg"
            image = Image.open(io.BytesIO(image_bytes))
            
            image_output_path = f"{output_folder}/image_page{page_num+1}_{img_index+1}.{image_ext}"
            image.save(image_output_path)

def read_all_pdf_files_in_folder(folder_path):

    pdf_files_path = os.path.join(folder_path, '*.pdf')
    pdf_files = glob.glob(pdf_files_path)
    i=1

    for pdf_file in pdf_files:
        
        all_pages_elements = extract_elements_order_from_pdf(pdf_file)
        extract_images_from_pdf(pdf_file, output_folder)
        txt=create_pagetxt(pdf_file,all_pages_elements)
        with open(txt_folder+"/file"+str(i)+".txt", 'w', encoding='utf-8') as file:
            file.write(txt)
        i+=1
        clear_folder()

read_all_pdf_files_in_folder(folder_path)








