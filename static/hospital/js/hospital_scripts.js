$(document).ready(function() {
        $('.hospital-detail-link').on('click', function(e) {
            e.preventDefault();

            var hospitalPk = $(this).data('hospital-pk');
            console.log(hospitalPk);

            $.ajax({
                type: 'GET',
                url: `/hospital/${hospitalPk}/`, // URL to fetch hospital detail
                success: function(data) {
                    $('.offcanvas').html(data);
                    var hospitalDetail = $('<div>').html(data); // Create a temporary element to parse the HTML content
                    var hospitalY = hospitalDetail.find('.div-detail').data('latitude');
                    var hospitalX = hospitalDetail.find('.div-detail').data('longitude');
                    console.log(hospitalY, hospitalX);

                    // panTo 함수 호출하여 해당 위치로 지도 이동
                    panTo(hospitalY, hospitalX)
                },
                error: function(xhr, status, error) {
                    console.error(error); // Handle errors if any
                }
            });
        });
    });