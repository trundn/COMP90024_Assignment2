function (doc) {
  if (doc.match_track_filter === true) {
    emit("Covid19", 1)
  } else {
    emit("Others", 1)
  }
}