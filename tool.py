import tkinter as tk
from tkinter import messagebox
import fetch_api
import main_script

def submit():
    pdf_link = entry_pdf.get()
    text = entry_text.get("1.0", tk.END)

    paper_id = pdf_link[pdf_link.rindex('/')+1:]


    if pdf_link and text:

        main_text, abstract = fetch_api.get_clean_text(paper_id)

        sentence_paragraph_scores_wo, paragraphs_wo_preprocessing = main_script.link_abstract_sentences_to_paragraphs(text,main_text)

        
        # Perform the necessary operations with the PDF link and text
        # You can add your code here to process the inputs as desired
        label_text_1 = tk.Label(window, text="Para 1 score: " + str(sentence_paragraph_scores_wo[0][0][0][0]), font=("Arial", 12))
        label_text_1.pack()
        entry_text_1 = tk.Text(window, height=4)
        entry_text_1.insert(tk.END, sentence_paragraph_scores_wo[0][0][0][1])
        entry_text_1.pack()

        label_text_2 = tk.Label(window, text="Para 2 score: " + str(sentence_paragraph_scores_wo[0][1][0][0]), font=("Arial", 12))
        label_text_2.pack()
        entry_text_2 = tk.Text(window, height=4)
        entry_text_2.insert(tk.END, sentence_paragraph_scores_wo[0][1][0][1])
        entry_text_2.pack()

        label_text_3 = tk.Label(window, text="Para 3 score: " + str(sentence_paragraph_scores_wo[0][2][0][0]), font=("Arial", 12))
        label_text_3.pack()
        entry_text_3 = tk.Text(window, height=4)
        entry_text_3.insert(tk.END, sentence_paragraph_scores_wo[0][2][0][1])
        entry_text_3.pack()


        #messagebox.showinfo("Success", "PDF link and text submitted successfully!")

    else:
        messagebox.showwarning("Warning", "Please enter both a PDF link and text.")

# Create the main window
window = tk.Tk()
window.title("Linking Abstract Sentences to Full-Text Paragraphs")

window_width = 800
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")


# Create a label and an entry widget for the PDF link
label_pdf = tk.Label(window, text="Paper Link:", font=("Arial", 12))
label_pdf.pack()
entry_pdf = tk.Entry(window, font=("Arial", 12))
entry_pdf.pack()

# Create a label and a text widget for the text
label_text = tk.Label(window, text="Text:", font=("Arial", 12))
label_text.pack()
entry_text = tk.Text(window, height=4, font=("Arial", 12))
entry_text.pack()

# Create a button for submitting the PDF link and text
submit_button = tk.Button(window, text="Submit", command=submit, font=("Arial", 12))
submit_button.pack()

# Create a label and a text widget for the text




# Start the main loop
window.mainloop()
