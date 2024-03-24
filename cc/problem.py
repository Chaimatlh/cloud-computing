from PyPDF2 import PdfFileReader, PdfFileWriter

def read_pdf(file_path):
    """Reads and prints the content of a PDF file."""
    with open(file_path, "rb") as file:
        pdf = PdfFileReader(file)
        num_pages = pdf.getNumPages()

        print(f"Number of pages: {num_pages}")

        for page_num in range(num_pages):
            page = pdf.getPage(page_num)
            text = page.extractText()
            print(f"Page {page_num + 1}:")
            print(text)

def write_pdf(file_path, content):
    """Writes the specified content to a new PDF file."""
    pdf = PdfFileWriter()
    pdf_writer.addPage()

    with open(file_path, "wb") as file:
        pdf.write(file)

    print(f"PDF file '{file_path}' created successfully.")

# Example usage
pdf_file_path = "sample.pdf"

# Read and print the content of the PDF file
read_pdf(pdf_file_path)

# Write a new PDF file with some content
new_pdf_file_path = "new_file.pdf"
content = "This is some sample content for the new PDF file."
write_pdf(new_pdf_file_path, content)

# Read and print the content of the new PDF file
read_pdf(new_pdf_file_path)


# read 3 fichiers pdf + xml + docs and method to  attacher any  fichiers service web et le prencipe des services 
# checksum 
# we have fichier pdf + plusier fichier nbaethom to service uresevier fichier ykhdamli fichier jdid o yatachli datat o yeaewd ybaethomli ++ app lazem naerf checksum taeha ++ app testi 
# ro7ha bro7ha (tests on python)
# ay 7aja tabaeth fi reseau tatbaet json 
# fichier json key +4 values 
# fichier pdfs to byte and collect on fichier json 
# check pdf have a checksum 
# in memory data base ykhabiw data fi lcloud bhadi tari9a 
# fichier tbaeto tglbo binaire tbaeto service yglbolk json data + checksum 
# dev api (swagger) +  cryptov + integrity (checksum)
# 34 ; fichier originzl + atach =
# apres les vacances 
# developement un probleme using the services application flask + cree loggin taeha   
# ki nbaet haja lel service lzm service ki yrj3lna yraj3  maeha fivhier log 



# hadi hia : nhazo deux fichier original + fichier attacher : 
  # 1 converter to binary 
  # 2 n7asbolhom checksum ta3hom
  # 3 nhazo n7otohom fi fichier json : ndiro key one org {value : binary + checksum} + key two attach {value : attach + checksum} , 
  # 4 nbaetoh fi un service (n3aytolo pdf attachement) , end point is the post 
  # 5 ki nbaeto fi l cote lokhr yverifier checksum + yhaz contenu tae fichier binaire o
  #  ykhamem winahom un fichier jdid w7d og y'attach dkhlo attch o hadi lkhdma binaire yb9a ykhdm binaire o yjeniri fichier
  # 6 fichier jdid , n7sblo checksum , n7oto fi fichier json , o naewd nbaeto 
  # end point ndirolo token 

#there are two sides involved:
#  the client side (the side that initiates the file upload) 
# and the server side (the Flask service that receives the file and performs further processing).
#  Typically, the client side sends the file upload request to the server side.