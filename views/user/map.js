function (doc) {
  if (doc.calculated_coordinates) {
    emit(doc.raw_data.user.id, doc.raw_data.user);
  }
}