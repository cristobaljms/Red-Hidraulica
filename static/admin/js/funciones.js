$(document).ready(function () {
    $('#beneficiarios_tabla').DataTable(
        {"language": {
            "lengthMenu": "Mostrar _MENU_ registros por pagina",
            "zeroRecords": "No hay registros",
            "info": "Mostrando pagina _PAGE_ de _PAGES_",
            "infoEmpty": "No records available",
            "infoFiltered": "(filtrado de _MAX_ registros totales)",
            "search":         "Buscar:",
            "paginate": {
                "first":      "Primero",
                "last":       "Ultimo",
                "next":       "Siguiente",
                "previous":   "Anterior"
            },
        }}
    );
});

// Active user
function borrarProyecto(pk){
    swal({
        title: "Eliminar proyecto1",
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
                    location.reload();
                }
              })
              return true;
        } else {
            swal("Operacion cancelada");
        }
    });
  }


// Active user
function borrarMaterial(pk){
    swal({
        title: "Eliminar material",
        text: "¿Seguro que desea borrar este material?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
        request_url = '/materiales/eliminar/' + pk
          $.ajax({
                url: request_url,
                success: function(data){
                    swal({title: "OK", text: 'Material borrado', type: "success", timer: 6000, allowEscapeKey:true});
                    location.reload();
                }
              })
              return true;
        } else {
            swal("Operacion cancelada");
        }
    });
  }

// Active user
function borrarFluido(pk){
    swal({
        title: "Eliminar fluido",
        text: "¿Seguro que desea borrar este fluido?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
        request_url = '/fluidos/eliminar/' + pk
          $.ajax({
                url: request_url,
                success: function(data){
                    swal({title: "OK", text: 'Fluido borrado', type: "success", timer: 6000, allowEscapeKey:true});
                    location.reload();
                }
              })
              return true;
        } else {
            swal("Operacion cancelada");
        }
    });
  }