        document.addEventListener('DOMContentLoaded', function(){
        var s = Snap("#avara");
        var paths = s.selectAll('path');
        var handle = s.select('#point-handle');
        paths.forEach(function(v, i) {
        for(var i=0, len=v.node.pathSegList.numberOfItems; i < len; i++){
            var el = v.node.pathSegList.getItem(i);
            if(typeof el.x != 'undefined'){
              var h = handle.use();
              h.attr({x:el.x,y:el.y})
              s.append(h)
              h.data('el', el);
              h.drag(
                function(dx,dy){
                  var tdx, tdy;
                  var snapInvMatrix = this.transform().diffMatrix.invert();
                  snapInvMatrix.e = snapInvMatrix.f = 0;
                  tdx = snapInvMatrix.x( dx,dy ); tdy = snapInvMatrix.y( dx,dy );
                  this.transform( this.data('ot') + "t" + [ tdx, tdy ]  );
                  this.data('el').x = this.data('ox')+tdx
                  this.data('el').y = this.data('oy')+tdy
                },
                function(){
                  this.data('ot', this.transform().local);
                  this.data('ox', this.data('el').x);
                  this.data('oy', this.data('el').y);
                }, null
              );
            }
          }
        });
      });
