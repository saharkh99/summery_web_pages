
import summery_pdf_quiz
import summary_website

def summery_quiz_from_pdf(path):
    return summery_pdf_quiz.read_pdf_and_summerize(path)

def read_pdf_from_url(url):
    return summary_website.scrape_with_playwright(url)


def main():
    print("Do you want to enter a PDF path or a URL?")
    choice = input("Enter 'path' or 'url': ").lower()

    if choice == 'path':
        pdf_path = input("Enter the path of the PDF file: ")
        text = summery_quiz_from_pdf(pdf_path)
    elif choice == 'url':
        pdf_url = input("Enter the URL of the PDF file: ")
        text = read_pdf_from_url(pdf_url)
    else:
        print("Invalid choice. Please enter 'path' or 'url'.")
        return

    print("\nText extracted from PDF:")
    print(text)

if __name__ == "__main__":
    main()