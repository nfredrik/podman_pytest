import docxtpl

# Create a new Docx-TPL template
template = docxtpl.DocxTemplate('template.docx')

# Load the PNG image as a base64-encoded string
with open('image.png', 'rb') as f:
    image_data = f.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

# Define the placeholder for the image in the template
template.add_placeholders({
    'image': {
        'type': 'image',
        'value': image_base64,
        'width': 200,  # Optional: set the width of the image
        'height': 100   # Optional: set the height of the image
    }
})

# Render the template with the placeholder
result = template.render()

# Save the resulting Word document to a file
with open('output.docx', 'wb') as f:
    f.write(result)