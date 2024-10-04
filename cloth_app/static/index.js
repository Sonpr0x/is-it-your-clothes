


$(document).ready(function() {
    resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
    document.querySelector('.btn-close').addEventListener('click', resultModal.hide());


    // Trigger event submit to show result
    $('#imageForm').submit(function(event) {
        event.preventDefault();
        var formData = new FormData(this);

        const resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
        resultImage = document.getElementById('resultimage'); 

        

        $.ajax({
            type: 'POST',
            url: '/process',
            data: formData,
            processData: false,
            contentType: false,
            success: function(result) {
                // Show the result layer and display the image
                resultModal.show();
                resultImage.src = 'data:image/jpeg;base64,' + result;
            }, 
        });
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

    // Delete image
    function deleteImage(imageId) {
        $.ajax({
            type: 'POST',
            url: `/delete_image/${imageId}`,
            success: function(response) {
                if (response.success) {
                    $(`.image-card[data-image-id=${imageId}]`).remove();

                    window.location.href = '/app';
                } else {
                    alert('Failed to delete the image.');
                }
            },
            error: function() {
                alert('Error occurred while deleting the image.');
            }
        });

    }

    
    









