function (doc) {
  if (doc.calculated_coordinates && doc.emotions) {
    var type = ""
    var emotion_value = -1
    if (doc.emotions.neg > emotion_value) {
      type = "NEGATIVE";
      emotion_value = doc.emotions.neg;
    }
    if (doc.emotions.neu > emotion_value) {
      type = "NEUTRAL";
      emotion_value = doc.emotions.neu;
    }
    if (doc.emotions.pos > emotion_value) {
      type = "POSITIVE";
      emotion_value = doc.emotions.pos;
    }

    emit(doc.calculated_coordinates, type, 1);
  }
}