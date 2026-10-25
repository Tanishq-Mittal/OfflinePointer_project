// JXA: glide the real mouse cursor to (x, y) in ~0.5 s. Point only, never clicks.
ObjC.import('CoreGraphics');
function run(argv) {
  var tx = parseFloat(argv[0]), ty = parseFloat(argv[1]);
  var cur = $.CGEventGetLocation($.CGEventCreate($()));
  var sx = cur.x, sy = cur.y, steps = 40;
  for (var i = 1; i <= steps; i++) {
    var t = i / steps; t = t * t * (3 - 2 * t);           // ease in/out
    $.CGWarpMouseCursorPosition($.CGPointMake(sx + (tx - sx) * t, sy + (ty - sy) * t));
    delay(0.01);
  }
}
