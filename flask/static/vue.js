var app = new Vue({
  delimiters : ['[[', ']]'],
  el: '#app',
  data : {
    game_state: game_state,
    selected_cell: null,
    selected_piece: null,
  },
  methods: {
    test: function(data) {
      console.log(data.piece)
    },
    select_cell: function(data) {
      this.selected_cell = data.position
    },
    select_piece: function(data) {
      this.selected_piece = data.piece
    },
    draw_game_board: function(row, col) {
      var canvas = document.getElementById("game_board");
      var ctx = canvas.getContext('2d');
      var cell_width = canvas.width/col;
      var cell_height = canvas.height/row;
      for (i=1; i<col; i++) {
        ctx.moveTo(cell_width*i, 0);
        ctx.lineTo(cell_width*i, canvas.height);
        ctx.stroke();
      }
      for (i=1; i<row; i++) {
        ctx.moveTo(0, cell_height*i);
        ctx.lineTo(canvas.width, cell_height*i);
        ctx.stroke();
      }
      for (i=0; i<this.game_state.board_pieces.length; i++) {
        var piece = this.game_state.board_pieces[i];
        var img = document.getElementById("im"+piece.piece);
        if (img != null) {
          console.log("draw image " + img.src + " at position " + piece.position);
          ctx.drawImage(img, piece.position[1]*cell_width, piece.position[0]*cell_height, 100, 100);
        }
      }

    },
    draw_available: function(row, col) {
      var canvas = document.getElementById("available");
      var ctx = canvas.getContext('2d');
      var cell_width = canvas.width/col;
      var cell_height = canvas.height/row;
      for (i=1; i<col; i++) {
        ctx.moveTo(cell_width*i, 0);
        ctx.lineTo(cell_width*i, canvas.height);
        ctx.stroke();
      }
      for (i=1; i<row; i++) {
        ctx.moveTo(0, cell_height*i);
        ctx.lineTo(canvas.width, cell_height*i);
        ctx.stroke();
      }
      for (i=0; i<row; i++) {
        for (j=0; j<col; j++) {
          var piece_number = i*8 + j;
          if (this.game_state.available[piece_number].img != null) {
            var img = document.getElementById("im"+piece_number);
            console.log("draw image " + img.src + " at position " + i*cell_height + "," + j*cell_width);
            ctx.drawImage(img, j*cell_width, i*cell_height, 50, 50);
          }
        }
      }
    },
    draw_selected: function () {
      var canvas = document.getElementById("selected");
      var ctx = canvas.getContext('2d');
      if (this.game_state.selected != null) {
        var img = document.getElementById("im"+this.game_state.selected.piece);
        console.log("selected is " + this.game_state.selected.piece);
        console.log("draw image " + img.src + " in selected");
        ctx.drawImage(img, 0, 0, 100, 100);
      }
    },
    click_cell: function() {
      var canvas = document.getElementById("game_board");
      var rect = canvas.getBoundingClientRect();
      var cell_width = canvas.width/4;
      var cell_height = canvas.height/4;
      var x = event.clientX - rect.left - 3;
      var y = event.clientY - rect.top - 3;

      if (x > canvas.width || y > canvas.height) { return true;}

      var row = Math.ceil(y / cell_height) - 1;
      var col = Math.ceil(x / cell_width) - 1;
      console.log("width: " + canvas.width + ", height: "+ canvas.height);
      console.log("X coords: " + x + ", Y coords: " + y);
      console.log("Row coords: " + row + ", Col coords: " + col);

      this.selected_cell = row*4 + col;
    },
    click_piece: function() {
      var canvas = document.getElementById("available");
      var rect = canvas.getBoundingClientRect();
      var cell_width = canvas.width/8;
      var cell_height = canvas.height/2;
      var x = event.clientX - rect.left - 3;
      var y = event.clientY - rect.top - 3;

      if (x > canvas.width || y > canvas.height) { return true;}

      var row = Math.ceil(y / cell_height) - 1;
      var col = Math.ceil(x / cell_width) - 1;
      console.log("width: " + canvas.width + ", height: "+ canvas.height);
      console.log("X coords: " + x + ", Y coords: " + y);
      console.log("Row coords: " + row + ", Col coords: " + col);

      this.selected_piece = row*8 + col;
    }

  }
});
window.onload = function () {
  app.draw_game_board(4, 4);
  app.draw_selected();
  app.draw_available(2, 8);
}
