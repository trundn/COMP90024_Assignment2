function (keys, values, rereduce) {
  if (rereduce) {
    var result = [];
    values.forEach(function (value) {
      value.forEach(function (point) {
          result.push(point);
        }
      )
    });

    var uniquePoints = [];
    result.forEach(function (point) {
        var existing = false;
        for (var i = 0; i < uniquePoints.length; i++) {
            if (uniquePoints[i][0] === point[0] && uniquePoints[i][1] === point[1]) {
                existing = true;
                break;
            }
        }

        if (existing === false) {
            uniquePoints.push(point);
        }
    });

    return uniquePoints;
  } else {
    return values;
  }
}