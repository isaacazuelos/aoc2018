#[derive(Debug)]
struct Instr(&'static str, usize, usize, usize);

impl Instr {
    fn execute(&self, reg: &mut [usize; 6]) {
        match self.0 {
            "addr" => reg[self.3] = reg[self.1] + reg[self.2],
            "addi" => reg[self.3] = reg[self.1] + self.2,
            "mulr" => reg[self.3] = reg[self.1] * reg[self.2],
            "muli" => reg[self.3] = reg[self.1] * self.2,
            "banr" => reg[self.3] = reg[self.1] & reg[self.2],
            "bani" => reg[self.3] = reg[self.1] & self.2,
            "borr" => reg[self.3] = reg[self.1] | reg[self.2],
            "bori" => reg[self.3] = reg[self.1] | self.2,
            "setr" => reg[self.3] = reg[self.1],
            "seti" => reg[self.3] = self.1,
            "gtri" => reg[self.3] = (reg[self.1] > self.2).into(),
            "gtir" => reg[self.3] = (self.1 > reg[self.2]).into(),
            "gtrr" => reg[self.3] = (reg[self.1] > reg[self.2]).into(),
            "eqri" => reg[self.3] = (reg[self.1] == self.2).into(),
            "eqir" => reg[self.3] = (self.1 == reg[self.2]).into(),
            "eqrr" => reg[self.3] = (reg[self.1] == reg[self.2]).into(),
            _ => panic!("unsupported insr: {:?}", self),
        }
    }
}

fn puzzle() -> Vec<Instr> {
    vec![
        Instr("addi", 2, 16, 2),
        Instr("seti", 1, 1, 5),
        Instr("seti", 1, 1, 3),
        Instr("mulr", 5, 3, 4),
        Instr("eqrr", 4, 1, 4),
        Instr("addr", 4, 2, 2),
        Instr("addi", 2, 1, 2),
        Instr("addr", 5, 0, 0),
        Instr("addi", 3, 1, 3),
        Instr("gtrr", 3, 1, 4),
        Instr("addr", 2, 4, 2),
        Instr("seti", 2, 8, 2),
        Instr("addi", 5, 1, 5),
        Instr("gtrr", 5, 1, 4),
        Instr("addr", 4, 2, 2),
        Instr("seti", 1, 5, 2),
        Instr("mulr", 2, 2, 2),
        Instr("addi", 1, 2, 1),
        Instr("mulr", 1, 1, 1),
        Instr("mulr", 2, 1, 1),
        Instr("muli", 1, 11, 1),
        Instr("addi", 4, 3, 4),
        Instr("mulr", 4, 2, 4),
        Instr("addi", 4, 7, 4),
        Instr("addr", 1, 4, 1),
        Instr("addr", 2, 0, 2),
        Instr("seti", 0, 4, 2),
        Instr("setr", 2, 8, 4),
        Instr("mulr", 4, 2, 4),
        Instr("addr", 2, 4, 4),
        Instr("mulr", 2, 4, 4),
        Instr("muli", 4, 14, 4),
        Instr("mulr", 4, 2, 4),
        Instr("addr", 1, 4, 1),
        Instr("seti", 0, 5, 0),
        Instr("seti", 0, 8, 2),
    ]
}

#[derive(Debug)]
struct State {
    ip: usize,
    ipp: usize,
    reg: [usize; 6],
    code: Vec<Instr>,
}

impl State {
    fn new() -> Self {
        State {
            ip: 0,
            ipp: 2, // from input
            reg: [0, 0, 0, 0, 0, 0],
            code: puzzle(),
        }
    }

    fn tick(&mut self) {
        // println!("{:?}", self);
        self.reg[self.ipp] = self.ip;
        let instr = &self.code[self.ip];
        instr.execute(&mut self.reg);
        self.ip = self.reg[self.ipp];
        self.ip += 1;
    }

    fn halted(&self) -> bool {
        self.ip > self.code.len()
    }

    fn run(&mut self) {
        while !self.halted() {
            self.tick();
        }
    }
}

fn part_1() {
    let mut state = State::new();
    state.run();
    println!("part 1: {}", state.reg[0]);
}

fn part_2() {
    let mut state = State::new();
    state.reg[0] = 1;
    state.run();
    println!("part 2: {}", state.reg[0]);
}

fn main() {
    part_1();
    part_2();
}
