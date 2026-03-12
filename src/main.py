from textnode import TextNode, TextType

def main():
    test = TextNode("this is text", TextType.link, "link.url.com")
    print(test)

if __name__ == "__main__":
    main()
