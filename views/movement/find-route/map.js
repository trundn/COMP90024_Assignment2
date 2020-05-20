function (doc) {
  if (doc.raw_data && doc.calculated_coordinates.length === 2) {
    var raw_data = doc.raw_data
    emit([raw_data.user.id, raw_data.user.screen_name], [[doc.calculated_coordinates[1], doc.calculated_coordinates[0]], doc.created_at], 1);
  }
}