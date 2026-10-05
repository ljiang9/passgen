#!/usr/bin/env python3
"""passgen: 本地密码 / 密码短语生成器。

使用 secrets 模块（CSPRNG），不使用 random。
不联网、不存储生成的密码——请把密码放进密码管理器。
"""
import argparse
import math
import secrets
import string
import sys

VERSION = "0.1.0"

UPPER = string.ascii_uppercase
LOWER = string.ascii_lowercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*-_=+[]{}:;,.<>?~"

# 精选英文单词表（~400 词）：简短、常见、无歧义拼写。
# 为诚实起见：此表小于 EFF 大单词表（7776 词），
# 每个单词的熵 = log2(词表大小)；详见 README。
WORDS = """abandon ability able about above absent absorb abstract absurd abuse access accident account accuse achieve acid acoustic acquire across act action actor actress actual adapt add admit adopt adult advance advice aerobic affair afford afraid again age agent agree ahead aim air alarm album alert alien align alive all alley allow almost alone along aloud alpha alter always amber amuse anger angle angry animal ankle apart apple apply arena argue arm armor army around arrange arrest arrive arrow art artist aspect assault asset assist assume asthma athlete atom attack attend august aunt auto autumn average avoid awake award aware awful baby back badge bag balance balcony ball bamboo banana banner bar barely barrel basic basket batch beach bean beard beast become bed before begin behave behind being believe bell belt bench benefit best betray better between beyond bicycle bid bike bind biology birth bitter black blade blame blanket blast blend bless blind block blood bloom blue blur board boat body boil bolt bomb bond bone bonus book boom boost booth border borrow boss bottom bounce bound bowl box boy bracket brain brand brass brave bread breeze brick bridge brief bright bring broad broke brown brush bubble buddy budget buffalo build bulb bulk bullet bundle bunker burden burst business butter button buyer cable cactus cage cake call calm camera camp cancel cannon canoe canvas canyon capable capital captain car carbon card cargo carpet carry catch cause caution cave ceiling celery center century cereal chair chalk chaos chapter charge chase cheap check cheese chest chicken chief child chimney choice choose chronic chunk churn cigar cinema circle citizen city civil claim clap clarify clash class clean clear clerk clever click cliff climb clock close cloth cloud clown club coach coast cobra code coffee coil coin collect color column combine come comfort comic commit common company concert conduct confirm congress connect consider control convince cook cool copper copy coral cost cotton couch could count couple course court cousin cover crack craft crash crater crawl crazy cream credit creek cricket crime crisp critic crop cross crowd crucial cruel cruise crumble crunch crush cry crystal cube culture cup curious current curve cushion custom cute cycle dad daily dairy damage dance danger daring dash daughter dawn day deal debate debris decade december decide declare decline decor deep deer delay deliver demand dense deny depart depend depth deputy derive describe desert design desk detail device devote diagram dial diamond diary dice differ digital dignity dilemma dinner direct dirt disagree discover disease dish dismiss dizzy doctor document dog doll domain donate donkey donor door dose double dove draft dragon drama drastic draw dream dress drill drink drive drop dry duck dumb dune during dust duty eager eagle early earth easily east easy echo ecology edit educate elbow elder elect elegant element elephant elite else email embark emerge employ empty enable enact end enemy energy engine enjoy enough ensure enter entire entry envelope equal equip era erase erode error erupt escape essay essence estate ethnic exact example excess exchange excite exclude excuse execute exercise exhaust exile exist exit exotic expand expect expire explain expose express extend extra eye eyebrow fabric fact faint faith false fame family famous fan fancy fatal father fault favor feast fence fetch fever few fiber fiction field fiend fierce fifty fight figure file fill film filter final find fine finger finish fire firm first fiscal fish fit five fix flag flame flash flask fleet flesh flight float flock floor flour fluid flush focus fold follow food foot force forest forget fork fortune forum forward fossil foster found fox fragile frame frank fraud fresh friend fringe frog front frost frown frozen fruit frustrate fuel fun funny giant given glacier globe glory glove glow glue goat goddess gold good goose gorge gossip govern gown grab grace grain grand grant grape grass grave great green greet grief grill grin grocery group grove guard guess guide guilt habit hair half hall hammer hamster hand happy harbor hard harsh harvest hat have hawk hazard head health heart heavy hedge height hello helmet help hen hero hidden hill hint hip hire history hobby hockey hold hole holiday hollow home honey honor hope horn horror horse hospital host hotel hour hover hub huge human humble humor hundred hungry hunt hurry hurt husband hybrid ice icon idea identify idle idol ignore ill illegal illness image imitate immense immune impact impose imply inch index indicate indoor industry infant inflict inform inhale inherit initial inject injury inner innocent input inquiry insane insect inside install intact interest into invite island issue ivory jacket jaguar jar jazz jelly jewel join joke judge juice jump jungle junior junk just kangaroo keen keep ketchup key kick kid kidney kind kingdom kiss kit kitchen kite kitten knee knife knock knot known lab label labor ladder lady lake lamp land lane language large later laugh launch law lawn layer lazy leader leaf learn leave lecture left legal legend leisure lemon lend length lens lesson letter level liar liberty library license life lift light like limb limit link lion liquid list little live lizard load loan local lock logic lonely long loop lord lose loss lost loud lounge love loyal lucky luggage lunar lunch luxury lyric machine magic magnet maiden mail main major make mammal manage manor march margin marine mark market marry mask mass master match material math matrix matter maximum maze meadow mean measure meat mechanic medal media melody melt member memory mention menu mercy merge merit merry metal method middle midnight might minor minus minute miracle mirror misery miss mistake mix mixed mixture mobile model modify mom moment monkey monster month moon moral more morning mosquito mother motion motor mountain mouse move movie much muffin mule multiply muscle museum mushroom music must mutual myself mystery myth naive name napkin narrow nation nature near neat neck need negative neglect neither nerve nest net never new news next nice night noble noise nominee noodle normal north nose notable note nothing notice novel now nuclear number nurse nut oak obey object oblige obtain ocean october odor off offer office often oil old olive olympic omit once one onion online only open opera opinion oppose option orange orbit order organ other outer output outside oval owner oxygen oyster ozone pact paddle page pair palace palm panda panel panic paper parent park parrot party pass patch path patrol pattern pause pave payment peace peanut pear pen pencil people pepper perfect permit person pet phone photo phrase physical piano picnic picture piece pig pilot pink pioneer pipe pistol pitch pizza place planet plastic plate plaza pleasant please pleasure pledge plenty pluck plug plunge poem poet point polar pole police pond pony pool popular portion position possible potato pottery poverty powder power practice praise predict prefer prepare present pretty prevent price pride primary print prior prize probe process produce profit program project promote proof property prosper protect proud prove public pudding pull pulp pulse punch pupil puppy purchase purity purple push put puzzle pyramid queen quick quit quiz quote rabbit raccoon race rack radar radio rail rain raise rally ramp ranch random range rapid rare rate rather raven raw razor ready real reason rebel recall receive recipe record reduce reflect reform refuse region regret regular reject relax release relief rely remain remark remind remove render renew rent repair repeat replace report rescue result retire retreat return reunion reveal review reward rhythm rib ribbon rice rich ride ridge rifle right rigid ring riot ripple risk ritual rival river road roast robot robust rocket roman roof rookie room rose rotate rough round route royal rubber ruler run runway rural sad saddle sadness safe sail salad salmon salon salt salute same sample sand satisfy sauce scale scan scare scene scent scheme school science scissor scout scrap screen screw script scrub sea search season seat second secret section sector secure seed seek segment select sell seminar senior sense sentence series serve service seven shade shadow shaft shall shape share shark sharp sheep sheet shelf shell shift shine shirt shock shoe shop short shoulder shout shove show shrimp shrug shuffle shy sibling sick side siege sight sign silent silk silly silver similar simple since sing sink sister sit six size skate sketch ski skill skin skirt skull slab sleep slice slide slight slim slogan slot slow slush small smart smell smile smoke smooth snack snake snap sneak solar soldier solid solve son song soon sorry sort soul sound source south space spare spark speak special speed spell spend sphere spice spider spike spin spirit split spoil sponsor spoon sport spot spray spread spring spy square squeeze stable stadium staff stage stair stamp stand start state stay steak steel steep steer stem step stereo stick still sting stock stomach stone stool story stove strategy street strike strong struggle student stuff stumble style subject submit subway success such sudden sugar suit summer sun sunny sunset super supply supreme sure surface surge surprise survey suspect swamp swap swarm swear sweet swift swim swing switch sword symbol syrup system table tackle tag tail talent talk tank tape target task taste tattoo taxi teach team tear tech tell ten tenant tennis tent term test text thank that theater theme there these thick thin thing think third thirst thirty thorn those though thought three thrive throw thumb thunder ticket tide tiger tight time tiny tip tired tissue title toast today toddler toe together toilet token told tomato tomorrow tone tongue tonight tool tooth top topic torch total touch tough tower town toy trace track trade traffic tragic train transfer trap trash travel tray treat trend trial tribe trick trigger trim trip trophy trouble truck truly trumpet trust truth try tube tulip tumble tuna tunnel turkey turn turtle twelve twenty twice twin twist two type typical ugly uncle uncover under undo unfair unfold unhappy union unique unit unite universe unknown unlock until upper upset urban urge usage useful usual utility valid valley valve van vanish vapor various vast vault vehicle velvet vendor venue verb verify verse version very vessel veteran viable vibrant vicious victory video view village violin virtual virus visa visit visual vital vivid vocal voice void volcano volume vote voyage wagon waist wait walk wall walnut want war warm warn wash wasp waste water wave way wealth weapon wear weasel weather web wedge week weigh weird welcome west wet whale what wheat wheel where which while whisper white whole who whose why wide width wife wild will win window wine wing winter wire wisdom wise wish witness wolf woman wonder wood wool word work world worry worth would wound wrap wreck wrestle wrist write wrong yard year yellow you young youth zebra zero zone zoo""".split()

WORD_COUNT = len(WORDS)


def password(length=20, symbols=True):
    """生成随机密码，保证每类字符至少出现一个。"""
    if length < 4:
        raise ValueError("长度至少为 4")
    classes = [UPPER, LOWER, DIGITS]
    pool = UPPER + LOWER + DIGITS
    if symbols:
        classes.append(SYMBOLS)
        pool += SYMBOLS
    chars = [secrets.choice(c) for c in classes]
    chars += [secrets.choice(pool) for _ in range(length - len(classes))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars), len(pool)


def pin(length=6):
    if length < 1:
        raise ValueError("长度至少为 1")
    return "".join(secrets.choice(DIGITS) for _ in range(length)), len(DIGITS)


def passphrase(count=5):
    if count < 1:
        raise ValueError("单词数至少为 1")
    words = [secrets.choice(WORDS) for _ in range(count)]
    return "-".join(words), WORD_COUNT


def entropy_bits(pool_size, length):
    return length * math.log2(pool_size)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="本地密码 / 密码短语生成器（secrets 模块，不联网、不存储）")
    ap.add_argument("--length", type=int, default=20, help="密码长度（默认 20）")
    ap.add_argument("--no-symbols", action="store_true", help="去掉符号字符")
    ap.add_argument("--pin", type=int, metavar="N",
                    help="生成 N 位纯数字 PIN")
    ap.add_argument("--passphrase", action="store_true",
                    help="生成单词密码短语（默认 5 个词）")
    ap.add_argument("--words", type=int, default=5, help="密码短语单词数（默认 5）")
    ap.add_argument("--count", type=int, default=1, help="生成几个（默认 1）")
    ap.add_argument("--entropy", action="store_true", help="显示熵（bits）")
    ap.add_argument("--version", action="version", version="passgen " + VERSION)
    args = ap.parse_args(argv)

    if args.count < 1:
        sys.stderr.write("error: --count 至少为 1\n")
        return 1

    for _ in range(args.count):
        if args.passphrase:
            secret, pool_size = passphrase(args.words)
            n = args.words
        elif args.pin is not None:
            secret, pool_size = pin(args.pin)
            n = args.pin
        else:
            secret, pool_size = password(args.length, not args.no_symbols)
            n = args.length
        line = secret
        if args.entropy:
            bits = entropy_bits(pool_size, n)
            if args.passphrase:
                line += "  [熵 ≈ %.1f bits：%d 个词 × log2(%d 词表)]" % (
                    bits, n, pool_size)
            else:
                line += "  [熵 ≈ %.1f bits：长度 %d × log2(%d 字符集)]" % (
                    bits, n, pool_size)
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
