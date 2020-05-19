function (doc) {
  if (doc.raw_data) {
    var raw_data = doc.raw_data
    emit([raw_data.user.id, raw_data.user.screen_name], [doc.calculated_coordinates, doc.created_at], 1);
  }
}