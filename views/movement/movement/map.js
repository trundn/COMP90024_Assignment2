function (doc) {
  if (doc.user && doc.calculated_coordinates) {
    if (doc.calculated_coordinates.length == 2) {
      emit(doc.user, doc.calculated_coordinates);
    }
  }
}