$(document).ready(function () {
    $('#beneficiarios_tabla').DataTable();
});

// Active user
function borrarProyecto(pk){
    swal({
        title: "Eliminar proyecto",
        text: "¿Seguro que desea borrar este proyecto?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
        request_url = '/proyectos/eliminar/' + pk
          $.ajax({
                url: request_url,
                success: function(data){
                    swal({title: "OK", text: 'Proyecto borrado', type: "success", timer: 6000, allowEscapeKey:true});
                    location.reload();
                }
              })
              return true;
        } else {
            swal("Operacion cancelada");
        }
    });
  }