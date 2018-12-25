#[derive(Debug, Clone, Copy)]
enum OpCode {
    Addr,
    Addi,
    Mulr,
    Muli,
    Banr,
    Bani,
    Borr,
    Bori,
    Setr,
    Seti,
    Gtri,
    Gtir,
    Gtrr,
    Eqri,
    Eqir,
    Eqrr,
}

#[derive(Debug)]
struct Instr(OpCode, usize, usize, usize);

impl Instr {
    fn execute(&self, reg: &mut [usize; 6]) {
        match self.0 {
            OpCode::Addr => reg[self.3] = reg[self.1] + reg[self.2],
            OpCode::Addi => reg[self.3] = reg[self.1] + self.2,
            OpCode::Mulr => reg[self.3] = reg[self.1] * reg[self.2],
            OpCode::Muli => reg[self.3] = reg[self.1] * self.2,
            OpCode::Banr => reg[self.3] = reg[self.1] & reg[self.2],
            OpCode::Bani => reg[self.3] = reg[self.1] & self.2,
            OpCode::Borr => reg[self.3] = reg[self.1] | reg[self.2],
            OpCode::Bori => reg[self.3] = reg[self.1] | self.2,
            OpCode::Setr => reg[self.3] = reg[self.1],
            OpCode::Seti => reg[self.3] = self.1,
            OpCode::Gtri => reg[self.3] = (reg[self.1] > self.2).into(),
            OpCode::Gtir => reg[self.3] = (self.1 > reg[self.2]).into(),
            OpCode::Gtrr => reg[self.3] = (reg[self.1] > reg[self.2]).into(),
            OpCode::Eqri => reg[self.3] = (reg[self.1] == self.2).into(),
            OpCode::Eqir => reg[self.3] = (self.1 == reg[self.2]).into(),
            OpCode::Eqrr => reg[self.3] = (reg[self.1] == reg[self.2]).into(),
        }
    }
    fn c_ify(&self) -> String {
        let names = ['a', 'b', 'c', 'd', 'i', 'e'];
        match self.0 {
            OpCode::Addr => format!("{} = {} + {};", names[self.3], names[self.1], names[self.2],),
            OpCode::Addi => format!("{} = {} + {};", names[self.3], names[self.1], self.2,),

            OpCode::Mulr => format!("{} = {} * {};", names[self.3], names[self.1], names[self.2],),
            OpCode::Muli => format!("{} = {} * {};", names[self.3], names[self.1], self.2,),

            OpCode::Banr => format!("{} = {} & {};", names[self.3], names[self.1], names[self.2],),
            OpCode::Bani => format!("{} = {} & {};", names[self.3], names[self.1], self.2,),

            OpCode::Borr => format!("{} = {} | {};", names[self.3], names[self.1], names[self.2],),
            OpCode::Bori => format!("{} = {} | {};", names[self.3], names[self.1], self.2,),

            OpCode::Setr => format!("{} = {};", names[self.3], names[self.1],),
            OpCode::Seti => format!("{} = {};", names[self.3], self.1,),

            OpCode::Gtri => format!("{} = ({} > {});", names[self.3], names[self.1], self.2),
            OpCode::Gtir => format!("{} = ({} > {});", names[self.3], self.1, names[self.2]),
            OpCode::Gtrr => format!("{} = ({} > {});", names[self.3], names[self.1], names[self.2]),

            OpCode::Eqri => format!("{} = ({} == {});", names[self.3], names[self.1], self.2),
            OpCode::Eqir => format!("{} = ({} == {});", names[self.3], self.1, names[self.2]),
            OpCode::Eqrr => format!("{} = ({} == {});", names[self.3], names[self.1], names[self.2]),
        }
    }
}

const INPUT: &[Instr] = &[
    Instr(OpCode::Seti, 123, 0, 5),
    Instr(OpCode::Bani, 5, 456, 5),
    Instr(OpCode::Eqri, 5, 72, 5),
    Instr(OpCode::Addr, 5, 4, 4),
    Instr(OpCode::Seti, 0, 0, 4),
    Instr(OpCode::Seti, 0, 7, 5),
    Instr(OpCode::Bori, 5, 65536, 3),
    Instr(OpCode::Seti, 733_884, 6, 5),
    Instr(OpCode::Bani, 3, 255, 1),
    Instr(OpCode::Addr, 5, 1, 5),
    Instr(OpCode::Bani, 5, 16_777_215, 5),
    Instr(OpCode::Muli, 5, 65899, 5),
    Instr(OpCode::Bani, 5, 16_777_215, 5),
    Instr(OpCode::Gtir, 256, 3, 1),
    Instr(OpCode::Addr, 1, 4, 4),
    Instr(OpCode::Addi, 4, 1, 4),
    Instr(OpCode::Seti, 27, 8, 4),
    Instr(OpCode::Seti, 0, 6, 1),
    Instr(OpCode::Addi, 1, 1, 2),
    Instr(OpCode::Muli, 2, 256, 2),
    Instr(OpCode::Gtrr, 2, 3, 2),
    Instr(OpCode::Addr, 2, 4, 4),
    Instr(OpCode::Addi, 4, 1, 4),
    Instr(OpCode::Seti, 25, 4, 4),
    Instr(OpCode::Addi, 1, 1, 1),
    Instr(OpCode::Seti, 17, 8, 4),
    Instr(OpCode::Setr, 1, 7, 3),
    Instr(OpCode::Seti, 7, 0, 4),
    Instr(OpCode::Eqrr, 5, 0, 1),
    Instr(OpCode::Addr, 1, 4, 4),
    Instr(OpCode::Seti, 5, 9, 4),
];

#[derive(Debug)]
struct State {
    ip: usize,
    ipp: usize,
    reg: [usize; 6],
    code: &'static [Instr],
}

impl State {
    fn new() -> Self {
        State {
            ip: 0,
            ipp: 4, // from input
            reg: [0, 0, 0, 0, 0, 0],
            code: INPUT,
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
    let mut label = 0;
    for instr in INPUT {
        println!("L{}: // {:?}", label, instr);
        println!("  {}", instr.c_ify());
        label += 1;
    }
}

fn part_2() {
    println!("part 2: unimplemented",);
}

fn main() {
    part_1();
    part_2();
}
