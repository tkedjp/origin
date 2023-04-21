class Monster:
    #コンストラクタ
    def __init__(self, init_hp):
        if (init_hp > 0):
            self.hp = init_hp
        else:
            print('体力は0以上です')
            self.hp = 1

    #攻撃する
    def damage(self, points):
        self.hp -=points
        if (self.hp < 0):
            return False
        else:
            return True

#継承（子供のクラスは親のクラスからは使えない）
class Wizard(Monster):
    def __init__(self, init_hp, init_mp):
        #上書きされたのでsuperによって親メソッドを呼び出し，init_hpを渡す
        super().__init__(init_hp)
        self.mp = init_mp

    #ここも上書き
    def damage(self, points):
        #防御力が高いので，攻撃が半分になる
        points /= 2
        super().damage(points)

    def magic(self):
        self.mp -= 10

goblin = Monster(50)

print('主人公の攻撃')
life = goblin.damage(10)
print('ゴブリンの体力は、'+ str(goblin.hp))
print('主人公の攻撃')
life = goblin.damage(60)
if (life == True):
    print('ゴブリンの体力は、'+ str(goblin.hp))
else:
    print('ゴブリンは倒れた')

#魔法使い（MPがある）
wizard01 =  Wizard(150, 70)

print('魔法使いが現れた 体力:' + str(wizard01.hp) + '/魔法使い:'+ str(wizard01.mp))
wizard01.damage(10)
print('魔法使いの体力は、'+ str(wizard01.hp))
print('魔法使いは魔法を唱えた')
wizard01.magic()
print('魔法使いの体力は、'+ str(wizard01.hp)+ '/魔法使い:'+ str(wizard01.mp))