function (doc) {
  if (doc.calculated_coordinates) {
    if (doc.calculated_coordinates.length == 2) {
      if (doc.match_track_filter) {
        emit(["With Coordinates", "covid"], 1)
      } else {
        emit(["With Coordinates", "basic"], 1)
      }
    } else {
      if (doc.match_track_filter) {
        emit(["Without Coordinates", "covid"], 1)
      } else {
        emit(["Without Coordinates", "basic"], 1)
      }
    }
  }
}