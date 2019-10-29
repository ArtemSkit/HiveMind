const fs = require('fs')
var list = {
  'M': 1,
  'T': 2,
  'W': 3,
  'R': 4,
  'F': 5,
  'S': 6
};
var res = []
var numberOfRecords = 500;
for (let index = 0; index < numberOfRecords; index++) {
  let days = Math.floor((Math.random() * 6) + 1);
  if (days == 6) record = Object.keys(list).join("");
  else {
    let temp = {}
    for (let index = 0; index < days; index++) {
      let day = Math.floor(Math.random() * 6);
      let dayStr = Object.keys(list)[day];
      temp[dayStr] = list[dayStr];
    }
    let tempRes = Object.keys(temp);
    tempRes.sort(function (a, b) {
      return temp[a] - temp[b];
    })
    res.push(tempRes.join(""));
  }
}
res = res.toString().replace(/,/g, '\n');
fs.writeFile('Output.txt', res, (err) => {

  // In case of a error throw err. 
  if (err) throw err;
})
