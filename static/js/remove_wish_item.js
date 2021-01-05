function delete_wish_item(wish_id){
       console.log(wish_id)
       var apiUrl = '/api/remove-wish-item/'+ wish_id;

       $.ajax({
            url: apiUrl,
            method: 'GET',
            success: function(result){
                var div_id = "wish_"+wish_id;
                $("#"+div_id).remove();
            }
       })

}