


$(document).ready(function() {

    // Trigger event submit to show result
    $('#image-form').submit(function(event) {
        event.preventDefault();
        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: '/app',
            data: formData,
            processData: false,
            contentType: false,
            success: function(result) {
                // Show the result layer and display the image
                $('#result-layer').show();
                $('#result-image').attr('src', 'data:image/jpeg;base64,' + result);
            }
        });
    });

    // Add an event listener to close the layer when the close button is clicked
    $('#close-layer').click(function() {
        $('#result-layer').hide();
    });
    

    // Get image upload data and read by preview element
    document.getElementById('person_image').addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('person_image_preview').src = e.target.result;
                document.getElementById('person_image_preview').classList.remove('d-none');
                document.getElementById('person_image_id').value = ''; 
            };
            reader.readAsDataURL(file);
        }
    });

    document.getElementById('cloth_image').addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('cloth_image_preview').src = e.target.result;
                document.getElementById('cloth_image_preview').classList.remove('d-none');
                document.getElementById('cloth_image_id').value = '';
            };
            reader.readAsDataURL(file);
        }
    });


    // listen click event to preview
    document.querySelectorAll('.card img').forEach((img) => {
        img.addEventListener('click', (event) => {
            const clickedImageSrc = event.target.src;
            const clickedImageType = event.target.dataset.imageType;
            const clickedImageId = event.target.dataset.imageId;

            if (clickedImageType === 'person') {
                document.getElementById('person_image_preview').src = clickedImageSrc;
                document.getElementById('person_image_id').value = clickedImageId;
                document.getElementById('person_image').value = '';
            } else if (clickedImageType === 'cloth') {
                document.getElementById('cloth_image_preview').src = clickedImageSrc;
                document.getElementById('cloth_image_id').value = clickedImageId; // Set the hidden input value
                document.getElementById('cloth_image').value = '';
            }

            // Remove the d-none class to make the preview image visible
            document.getElementById(`${clickedImageType}_image_preview`).classList.remove('d-none');
        });
    });

    });









