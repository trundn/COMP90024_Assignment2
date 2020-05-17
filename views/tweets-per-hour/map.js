function (doc) {
  if (doc.raw_data) {
    var data = doc.raw_data;
    var date = new Date(data.created_at)
    var hour = date.getHours()
    emit(hour, 1);
  }
}