let blackHole;
let stars = [];
let G = 1; 

function setup() {
  createCanvas(windowWidth, windowHeight);
  blackHole = new BlackHole(width / 2, height / 2, 5000);
  for (let i = 0; i < 300; i++) {
    stars.push(new Star(random(width), random(height), random(1, 5)));
  }
}

function draw() {
  background(0);

  blackHole.show();

  for (let s of stars) {
    blackHole.pull(s);
    s.update();
    s.show();
  }

  stars = stars.filter(s => !s.dead);
}

//class for black hole
class BlackHole {
  constructor(x, y, mass) {
    this.pos = createVector(x, y);
    this.mass = mass;
    this.rs = this.mass * 0.01; // Schwarzschild radius (scaled)
  }

  pull(star) {
    let force = p5.Vector.sub(this.pos, star.pos);
    let r = force.mag();
    let strength = (G * this.mass * star.mass) / (r * r);
    force.setMag(strength);
    star.applyForce(force);

    if (r < this.rs) star.dead = true;
  }

  show() {
    noStroke();
    fill(0);
    ellipse(this.pos.x, this.pos.y, this.rs * 2);
    stroke(255, 100, 150, 150);
    noFill();
    ellipse(this.pos.x, this.pos.y, this.rs * 4); // glowing effect
  }
}

class Star {
  constructor(x, y, mass) {
    this.pos = createVector(x, y);
    this.vel = p5.Vector.random2D().mult(random(0.5, 2));
    this.acc = createVector(0, 0);
    this.mass = mass;
    this.dead = false;
  }

  applyForce(f) {
    this.acc.add(p5.Vector.div(f, this.mass));
  }

  update() {
    this.vel.add(this.acc);
    this.pos.add(this.vel);
    this.acc.mult(0);
  }

  show() {
    noStroke();
    fill(255, 255, 200);
    ellipse(this.pos.x, this.pos.y, this.mass * 2);
  }
}
// return 0;
