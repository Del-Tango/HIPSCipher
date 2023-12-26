**HIPSCipher - Encryption/Decryption**

[ **DESCRIPTION** ]: Cipher Automation Tool for image based steganography.

[ **NOTE** ]: Steganography is the art and science of concealing information within seemingly neutral data in order to keep the existence of the information confidential. In the context of digital images, image-based steganography involves hiding data within image files without visibly altering the original image.

[ **NOTE** ]: EXIF (Exchangeable image file format) is a standard for storing metadata in image files, including details such as camera settings, date and time, and geolocation. Manipulating EXIF data in images is another form of steganography, often used for information hiding or tampering.

[ **EXAMPLES** ]: Running as a standalone script

    [ Ex ]: Terminal based running mode with default settings
       ~$ ./hips_cipher.py

    [ Ex ]: File based running mode decryption
       ~$ ./hips_cipher.py \
           --action decrypt \
           --image-file ./dta/Regards.jpg \
           --key-code HIPS1234

    [ Ex ]: File based running mode encryption with no STDOUT
       ~$ ./hips_cipher.py \
           --action encrypt \
           --image-file ./dta/Regards.jpg \
           --key-code HIPS1234 \
           --cleartext-file hc_cleartext.txt \
           --in-place \
           --silent

    [ Ex ]: File based running mode batch encryption with STDOUT
       ~$ ./hips_cipher.py \
           --action encrypt \
           --key-code HIPS1234 \
           --batch \
           --batch-dir files2encrypt \
           --cleartext-file hc_cleartext.txt

   [ Ex ]: File based EXIF dump saved to non-default report file
       ~$ ./hips_cipher.py \
           --action dump-exif \
           --image-file ./dta/Regards.jpg \
           --report \
           --report-file hc_custom.report

   [ Ex ]: File based EXIF write
       ~$ ./hips_cipher.py \
           --action write-exif \
           --exif-tag 37510 \
           --exif-data #!/ \
           --image-file ./dta/Regards.jpg

   [ Ex ]: File based EXIF tag read
       ~$ ./hips_cipher.py \
           --action read-exif \
           --exif-tag 37510 \
           --image-file ./dta/Regards.jpg

   [ Ex ]: File based EXIF cleanup
       ~$ ./hips_cipher.py \
           --action clean-exif \
           --image-file ./dta/Regards.jpg

   [ Ex ]: Run with context data from JSON config file
       ~$ ./hips_cipher.py \
           --konfig-file conf/hips_cipher.conf.json

   [ Ex ]: Cleanup all generated files from disk
       ~$ ./hips_cipher.py \
           --action cleanup

[ **EXAMPLES** ]: Building consumable artifact

    [ Ex ]: Cleanup build files with no manual interaction, install dependencies, ensure project file structure, build Python3 package and install it in a virtual environment using pip -

        ~$ ./build.sh --cleanup -y --setup BUILD INSTALL

    [ Ex ]: Run project autotesters -

        ~$ ./build.sh --test

[ **EXAMPLES** ]: Running as a system util (requires package build and install)

    [ Ex ]: Run in interactive mode using the terminal as a data source

        ~$ hipscipher

    [ Ex ]: Run using the parameters specified in the config file

        ~$ hipscipher --konfig-file conf/hips_cipher.conf.json

[ **NOTE** ]: For more details on how to use this damn thing along with screenshots you can read the DOX, maybe even using the dox-reader tool (*if you're brave enough*) -

    [ Ex ]: Change directory and execute dox-reader tool -

        ~$ cd ./dox && ./dox-reader.sh


Excellent Regards,

