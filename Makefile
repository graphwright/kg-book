all: outline.epub outline.pdf

clean:
	rm -f outline.epub outline.pdf

outline.epub: outline.md CoverImage.png ExampleGraph.png
	pandoc outline.md --metadata title="Knowledge Graphs from Unstructured Text" -o outline.epub

outline.pdf: outline.md CoverImage.png ExampleGraph.png
	pandoc outline.md -t latex --metadata title="Knowledge Graphs from Unstructured Text" -o outline.pdf
