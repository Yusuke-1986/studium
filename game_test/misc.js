// キー操作
document.onkeydown = function(e){
    key[e.keyCode] = true;
    if(gameOver && e.keyCode == 82){
        delete jiki;
        jiki = new Jiki();
        gameOver = false;
        score = 0;
    }
}
document.onkeyup = function(e){
    key[e.keyCode] = false;
}

// rand関数の定義
function rand(min, max){
    return Math.floor(Math.random() * (max-min+1))+min;
}

// スプライトの描画
function drawSprite( snum, x, y){
    let sx = sprite[snum].x;
    let sy = sprite[snum].y;
    let sw = sprite[snum].w;
    let sh = sprite[snum].h;
    
    let px = (x >> 8) - sw/2;
    let py = (y >> 8) - sh/2;

    if(px + sw <camera_x || px >camera_x+SCREEN_W || py + sh < camera_y || py >camera_y+SCREEN_H) return;

    vcon.drawImage(spriteImage, sx, sy, sw, sh, px, py, sw, sh);
}

// 当たり判定計算
function checkHit(x1, y1, r1, x2, y2, r2){
    
    let a = (x1 - x2) >> 8;
    let b = (y1 - y2) >> 8;
    let r = r1 + r2;

    return (r*r >= a*a + b * b);
}

// キャラクタ定義クラス
class CharaBase{
    constructor(snum, x, y, vx, vy){
        this.sn = snum;
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.kill = false;
        this.count = 0;
    }
    // 更新処理
    update(){
        this.count++;

        this.x += this.vx;
        this.y += this.vy;

        if(this.x+(100<<8) < 0 || this.x-(100<<8) > FIELD_W << 8 || this.y+(100<<8) < 0 || this.y-(100<<8) > FIELD_H << 8){
            this.kill = true;
        }
    }
    // 描画処理
    draw(){
        drawSprite(this.sn, this.x, this.y);
    }
}

// 爆発定義クラス(CharBase継承)
class Expl extends CharaBase{
    constructor(c, x, y, vx, vy){
        super(0, x, y, vx, vy);
        this.timer = c;
    }
    update(){
        if(this.timer){
            this.timer--;
            return;
        }
        super.update();
    }
    draw(){
        if(this.timer) return;

        this.sn = 16 + (this.count >> 2);
        if(this.sn == 27){
            this.kill = true;
            return;
        }
        super.draw();
    }

}

// 爆発処理
function explosion(x, y, vx, vy){
    expl.push( new Expl(0, x, y, vx, vy));
    for(let i = 0; i < 10; i++){
        let evx = vx + (rand(-10, 10) << 6);
        let evy = vy + (rand(-10, 10) << 6);
        expl.push( new Expl(i, x, y, evx, evy));
    }
    

}

// 星の定義クラス
class Star{
    constructor(){
        this.x = rand(0, FIELD_W) << 8;
        this.y = rand(0, FIELD_H) << 8;
        this.vx = 0;
        this.vy = rand(100, 300);
        this.sz = rand(1,2);
    }

    draw(){
        let x = this.x >> 8;
        let y = this.y >> 8;
        if(x<camera_x || x>camera_x+SCREEN_W || y<camera_y || y>camera_y+SCREEN_H) return;
        vcon.fillStyle = rand(0,2) != 0?"66f":"#8af";
        vcon.fillRect(this.x >> 8, this.y >> 8, this.sz, this.sz);

    }

    update(){
        this.x += this.vx * starSpeed / 100;
        this.y += this.vy * starSpeed / 100;
        if(this.y > FIELD_H << 8 ){
            this.y = 0;
            this.x = rand(0, FIELD_W) << 8;
        }
    }
}
