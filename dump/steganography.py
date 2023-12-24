

from PIL import Image
from stegano import lsb

def detect_steganography(image_path):
    try:
        image = Image.open(image_path)
        decoded_text = lsb.reveal(image)

        if decoded_text:
            print("Steganography detected!")
            print("Hidden message:", decoded_text)
        else:
            print("No steganography detected.")

    except Exception as e:
        print("Error:", e)

# Example usage:
image_path = "path/to/your/image.jpg"
detect_steganography(image_path)


from PIL import Image
from stegano import lsb

def add_steganography(image_path, output_path, message):
    try:
        # Open the image
        image = Image.open(image_path)

        # Encode the message into the image using LSB steganography
        encoded_image = lsb.hide(image, message)

        # Save the output image
        encoded_image.save(output_path)

        print("Steganography message added successfully!")

    except Exception as e:
        print("Error:", e)

# Example usage:
original_image_path = "path/to/your/original_image.jpg"
output_image_path = "path/to/your/output_image_with_steganography.jpg"
message_to_hide = "This is a hidden message."

add_steganography(original_image_path, output_image_path, message_to_hide)


