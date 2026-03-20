from __future__ import annotations

GLOBAL_PROMPT_STYLE = (
    '高品质幻想生物游戏立绘，主机级3A概念设定图，非Q版，非儿童向，成熟审美，'
    'PBR材质与高光金属细节，体积光，电影级边缘光，清晰轮廓，结构准确，细节密度高'
)

GLOBAL_PROMPT_COMPOSITION = (
    '单体角色，全身完整入镜，居中构图，正视或三分之二视角，动态姿态，'
    '四周留白适中，主体边缘干净，不裁切头尾，不出现多余角色'
)

GLOBAL_PROMPT_OUTPUT = (
    '透明背景，PNG，1024x1024，禁止背景场景，禁止地面、禁止边框、禁止文字、'
    '禁止logo、禁止水印、禁止UI元素'
)

GLOBAL_NEGATIVE_PROMPT = (
    '低清晰度，模糊，噪点，过曝，欠曝，畸形肢体，比例错误，重复肢体，'
    '幼儿绘本风，低龄萌宠头像风，搞笑表情包风，廉价卡通，像素风'
)

STAGE_ART_DIRECTION: dict[int, str] = {
    1: '初始形态：简洁克制，核心识别特征明确，装备和能量特效较少但有质感。',
    2: '进化形态：强化主特征，增加发光纹路与能量流，装备复杂度提升。',
    3: '超进化形态：明显华丽化，加入多层符文结构、灵体粒子、史诗级压迫感。',
    4: '究极进化形态：终极皮肤级别，传奇王者气场，复杂高阶饰甲与多层能量结构。',
}


def _expand_image_prompt(
    pet_name: str,
    pet_type: str,
    rarity: str,
    stage_index: int,
    stage_name: str,
    stage_description: str,
    core_prompt: str,
) -> str:
    stage_direction = STAGE_ART_DIRECTION.get(stage_index, STAGE_ART_DIRECTION[1])
    return (
        f'角色名称：{pet_name}；类型：{pet_type}；稀有度：{rarity}；'
        f'阶段：第{stage_index}阶段「{stage_name}」。'
        f'阶段描述：{stage_description}。'
        f'核心视觉关键词：{core_prompt}。'
        f'风格要求：{GLOBAL_PROMPT_STYLE}。'
        f'阶段美术方向：{stage_direction}'
        f'构图要求：{GLOBAL_PROMPT_COMPOSITION}。'
        f'输出要求：{GLOBAL_PROMPT_OUTPUT}。'
        f'负面约束：{GLOBAL_NEGATIVE_PROMPT}。'
    )


PET_TEMPLATE_SEED: list[dict] = [
    {
        'id': 1,
        'name': '霆曜狮鹫',
        'pet_type': '雷光战灵',
        'lore': '诞生于风暴断层的契约战兽，能够以雷羽刻印主人的战斗意志。',
        'rarity': '史诗',
        'image_url': None,
        'stages': [
            {
                'stage_index': 1,
                'stage_key': 'base',
                'stage_name': '裂风幼翼',
                'stage_description': '翼骨纤长、羽端带电，能在短距离冲刺中留下蓝白电痕。',
                'image_prompt': '幻想生物，狮鹫幼体，冷金属羽片与蓝白电纹，深色背景，高品质游戏立绘，克制但有力量感',
                'level_min': 1,
                'level_max': 9,
            },
            {
                'stage_index': 2,
                'stage_key': 'evolved',
                'stage_name': '奔雷狮鹫',
                'stage_description': '肩甲与翼刃成形，冲锋时可牵引雷弧，战场机动性显著提升。',
                'image_prompt': '幻想战宠，进化狮鹫，翼刃发光纹路，元素能量环绕，青蓝雷电粒子，游戏角色设定图，精致描边',
                'level_min': 10,
                'level_max': 19,
            },
            {
                'stage_index': 3,
                'stage_key': 'ascended',
                'stage_name': '天穹霆主',
                'stage_description': '体表覆以符文铠羽，双翼展开可形成雷暴穹顶，具备区域压制能力。',
                'image_prompt': '超进化狮鹫，华丽饰甲，雷暴核心，神秘符文，灵体粒子，史诗级进化，深蓝黑环境，传说皮肤质感',
                'level_min': 20,
                'level_max': 99,
            },
            {
                'stage_index': 4,
                'stage_key': 'ultimate',
                'stage_name': '万霆裁决皇',
                'stage_description': '王冠状雷角与多重能量翼同现，落翼即降天罚，具终局压迫感。',
                'image_prompt': '究极进化幻想狮鹫，终极皮肤级别，雷电王冠，层叠能量翼，金蓝闪光，史诗战场构图，高级游戏立绘设定稿',
                'level_min': 100,
                'level_max': None,
            },
        ],
    },
    {
        'id': 2,
        'name': '玄潮鲸灵',
        'pet_type': '深海灵兽',
        'lore': '来自古海神殿遗迹的潮汐守望者，以水压与声波共振塑造护盾。',
        'rarity': '传说',
        'image_url': None,
        'stages': [
            {
                'stage_index': 1,
                'stage_key': 'base',
                'stage_name': '潮核幼灵',
                'stage_description': '半透明躯体中悬浮潮汐核心，行动安静却拥有稳定治愈气场。',
                'image_prompt': '幻想鲸灵幼体，半透明水体，青色光核，深海粒子，克制高级感，游戏立绘',
                'level_min': 1,
                'level_max': 9,
            },
            {
                'stage_index': 2,
                'stage_key': 'evolved',
                'stage_name': '渊潮巡游者',
                'stage_description': '鳍翼生出流线护甲，可在队友周围形成旋涡屏障并反射冲击。',
                'image_prompt': '进化鲸灵，流线装甲，旋涡能量护盾，青蓝水纹发光，幻想契约兽，高品质设定图',
                'level_min': 10,
                'level_max': 19,
            },
            {
                'stage_index': 3,
                'stage_key': 'ascended',
                'stage_name': '深渊潮皇',
                'stage_description': '体长倍增，背脊符文点亮，掀起潮汐壁垒并控制广域战线。',
                'image_prompt': '超进化深海鲸灵，巨型体态，符文背脊，深海神殿背景，灵体粒子与水雾，史诗感游戏立绘',
                'level_min': 20,
                'level_max': 99,
            },
            {
                'stage_index': 4,
                'stage_key': 'ultimate',
                'stage_name': '寂海神谕者',
                'stage_description': '周身悬浮古代水环与圣纹，吟唱时可冻结时间般压制敌方节奏。',
                'image_prompt': '究极鲸灵，传说级皮肤质感，古海神谕符文，悬浮水环与光带，终极形态，电影级构图，游戏立绘设定稿',
                'level_min': 100,
                'level_max': None,
            },
        ],
    },
    {
        'id': 3,
        'name': '灰烬翼龙',
        'pet_type': '炎核战宠',
        'lore': '火山裂隙中被封印的翼龙血脉，越战越灼，拥有失控边缘的爆发力。',
        'rarity': '史诗',
        'image_url': None,
        'stages': [
            {
                'stage_index': 1,
                'stage_key': 'base',
                'stage_name': '灼鳞雏龙',
                'stage_description': '鳞甲呈暗红岩纹，吐息带细碎火星，力量尚在积蓄阶段。',
                'image_prompt': '幻想翼龙幼体，暗红岩鳞，微量火花，深灰背景，硬朗线条，游戏设定稿风格',
                'level_min': 1,
                'level_max': 9,
            },
            {
                'stage_index': 2,
                'stage_key': 'evolved',
                'stage_name': '熔脉翼龙',
                'stage_description': '翼骨扩展，胸腔熔核可见，俯冲时形成高温焰尾。',
                'image_prompt': '进化翼龙，熔岩脉络发光，橙红焰尾，元素能量包裹，战宠立绘，质感金属鳞片',
                'level_min': 10,
                'level_max': 19,
            },
            {
                'stage_index': 3,
                'stage_key': 'ascended',
                'stage_name': '焚天炎爵',
                'stage_description': '背脊长出熔晶尖角，火翼如刃，拥有范围焚烧与空域压制能力。',
                'image_prompt': '超进化火焰翼龙，华丽熔晶饰甲，火翼刀刃，史诗级进化，暗场高对比，传说皮肤质感',
                'level_min': 20,
                'level_max': 99,
            },
            {
                'stage_index': 4,
                'stage_key': 'ultimate',
                'stage_name': '终焰龙皇',
                'stage_description': '体表流动白金火纹，展开灾厄级火域，宛如末日审判降临。',
                'image_prompt': '究极火焰龙皇，白金火纹与烈焰王冠，终极皮肤级别，毁灭战场，复杂能量层次，高级游戏立绘',
                'level_min': 100,
                'level_max': None,
            },
        ],
    },
    {
        'id': 4,
        'name': '星穹狐',
        'pet_type': '奥术灵兽',
        'lore': '栖息于星术回廊的九尾契灵，擅长操控幻象与空间折跃。',
        'rarity': '稀有',
        'image_url': None,
        'stages': [
            {
                'stage_index': 1,
                'stage_key': 'base',
                'stage_name': '星纹幼狐',
                'stage_description': '尾端闪烁细碎星点，能短暂扭曲感知，让敌人判断失误。',
                'image_prompt': '幻想幼狐，星纹尾巴，微弱奥术光点，深色舞台光，高级插画感游戏设定',
                'level_min': 1,
                'level_max': 9,
            },
            {
                'stage_index': 2,
                'stage_key': 'evolved',
                'stage_name': '星轨幻狐',
                'stage_description': '形成三重光尾与法阵印记，具备中距离位移和幻影分身。',
                'image_prompt': '进化奥术狐，星轨尾光，符文法阵，青紫能量，幻想伙伴，高品质游戏角色立绘',
                'level_min': 10,
                'level_max': 19,
            },
            {
                'stage_index': 3,
                'stage_key': 'ascended',
                'stage_name': '寰宇秘尾',
                'stage_description': '九尾齐现并附着星屑护甲，可开辟短时星门改变战场站位。',
                'image_prompt': '超进化九尾灵兽，星门特效，华丽符文护甲，灵体粒子飘散，史诗构图，传说皮肤质感',
                'level_min': 20,
                'level_max': 99,
            },
            {
                'stage_index': 4,
                'stage_key': 'ultimate',
                'stage_name': '天象裁梦者',
                'stage_description': '尾部化作星环冠冕，执掌梦境与现实边界，拥有神话级控制力。',
                'image_prompt': '究极奥术九尾，终极形态，星环冠冕，天象投影，层叠光效，传说级游戏立绘设定稿',
                'level_min': 100,
                'level_max': None,
            },
        ],
    },
    {
        'id': 5,
        'name': '岩誓巨犀',
        'pet_type': '大地守卫',
        'lore': '与古代城邦签订守护誓约的战犀，能把冲锋转化为守护结界。',
        'rarity': '稀有',
        'image_url': None,
        'stages': [
            {
                'stage_index': 1,
                'stage_key': 'base',
                'stage_name': '岩角幼犀',
                'stage_description': '岩角尚短但质地坚硬，擅长近身顶撞与地面震颤。',
                'image_prompt': '幻想岩犀幼体，石质短角，厚重感，炭灰背景，硬派游戏立绘',
                'level_min': 1,
                'level_max': 9,
            },
            {
                'stage_index': 2,
                'stage_key': 'evolved',
                'stage_name': '磐壁战犀',
                'stage_description': '背甲扩展成盾墙结构，能在冲锋后生成半圆防护壁。',
                'image_prompt': '进化战犀，岩石装甲，金色裂纹发光，防御护壁特效，幻想战宠设定图',
                'level_min': 10,
                'level_max': 19,
            },
            {
                'stage_index': 3,
                'stage_key': 'ascended',
                'stage_name': '地脉堡垒兽',
                'stage_description': '脊背浮现地脉符文塔，能够调动大地之力形成多层防线。',
                'image_prompt': '超进化岩系巨犀，地脉符文塔，华丽重甲，史诗防御气场，尘土与光粒子，游戏级立绘',
                'level_min': 20,
                'level_max': 99,
            },
            {
                'stage_index': 4,
                'stage_key': 'ultimate',
                'stage_name': '不朽山王',
                'stage_description': '化身移动山岳，角尖缠绕金石圣纹，压场能力达到传说上限。',
                'image_prompt': '究极大地守卫，山岳级体量，金石圣纹与王者护甲，终极皮肤质感，震撼战场构图，高级游戏立绘',
                'level_min': 100,
                'level_max': None,
            },
        ],
    },
    {
        'id': 6,
        'name': '影缚夜鸦',
        'pet_type': '暗影契兽',
        'lore': '被月蚀仪式唤醒的影鸦，可吞噬光线并封锁敌方行动轨迹。',
        'rarity': '史诗',
        'image_url': None,
        'stages': [
            {
                'stage_index': 1,
                'stage_key': 'base',
                'stage_name': '黯羽幼鸦',
                'stage_description': '羽色如墨，眼底有细微紫辉，擅长侦察与潜入。',
                'image_prompt': '幻想暗影乌鸦幼体，墨色羽毛，紫色微光眼，神秘氛围，游戏角色设定图',
                'level_min': 1,
                'level_max': 9,
            },
            {
                'stage_index': 2,
                'stage_key': 'evolved',
                'stage_name': '蚀月影鸦',
                'stage_description': '翼缘出现月蚀符印，飞掠时可短暂沉默目标技能。',
                'image_prompt': '进化暗影夜鸦，月蚀符印，黑紫能量羽刃，发光纹路，幻想契约兽，高质感立绘',
                'level_min': 10,
                'level_max': 19,
            },
            {
                'stage_index': 3,
                'stage_key': 'ascended',
                'stage_name': '虚界渡鸦',
                'stage_description': '身形可在实体与灵体间切换，携带影链封印敌方核心单位。',
                'image_prompt': '超进化暗影渡鸦，灵体粒子，影链缠绕，华丽黑金饰羽，史诗压迫感，传说皮肤风格',
                'level_min': 20,
                'level_max': 99,
            },
            {
                'stage_index': 4,
                'stage_key': 'ultimate',
                'stage_name': '夜蚀审判者',
                'stage_description': '展开双重影翼与环月王印，能够主导整片战场光影法则。',
                'image_prompt': '究极暗影神鸦，终极皮肤级别，黑金双翼，环月王印，神秘符文风暴，电影质感游戏立绘',
                'level_min': 100,
                'level_max': None,
            },
        ],
    },
    {
        'id': 7,
        'name': '苍岚鹿',
        'pet_type': '风木灵兽',
        'lore': '守望古林风脉的灵鹿，能将风与生命力编织为战场支援结界。',
        'rarity': '稀有',
        'image_url': None,
        'stages': [
            {
                'stage_index': 1,
                'stage_key': 'base',
                'stage_name': '岚芽灵鹿',
                'stage_description': '角端生嫩绿光芽，移动时拖曳轻风轨迹，治疗能力初显。',
                'image_prompt': '幻想灵鹿幼体，风叶光芽，清冷青绿能量，深色森林背景，游戏设定图',
                'level_min': 1,
                'level_max': 9,
            },
            {
                'stage_index': 2,
                'stage_key': 'evolved',
                'stage_name': '风林巡誓者',
                'stage_description': '鹿角延展成分叉风冠，可召唤林风护场并强化队伍续航。',
                'image_prompt': '进化风木灵鹿，分叉风冠鹿角，青蓝风纹，能量叶片飘散，幻想伙伴立绘',
                'level_min': 10,
                'level_max': 19,
            },
            {
                'stage_index': 3,
                'stage_key': 'ascended',
                'stage_name': '苍穹森灵王',
                'stage_description': '角冠化作浮空枝晶，脚下生成森林法阵，兼具回复与控制。',
                'image_prompt': '超进化灵鹿王，浮空枝晶角冠，森林法阵，华丽自然符文，史诗级进化，高级游戏立绘',
                'level_min': 20,
                'level_max': 99,
            },
            {
                'stage_index': 4,
                'stage_key': 'ultimate',
                'stage_name': '万木天启者',
                'stage_description': '背后显现生命古树幻影，风木双系能量融合，拥有神域级守护。',
                'image_prompt': '究极风木灵兽，生命古树幻影，神域守护光环，终极皮肤质感，青金能量层叠，游戏立绘设定稿',
                'level_min': 100,
                'level_max': None,
            },
        ],
    },
    {
        'id': 8,
        'name': '霜烬白虎',
        'pet_type': '冰炎双生',
        'lore': '被双极元素淬炼的白虎机甲灵，冰与火在其体内达成危险平衡。',
        'rarity': '传说',
        'image_url': None,
        'stages': [
            {
                'stage_index': 1,
                'stage_key': 'base',
                'stage_name': '霜纹幼虎',
                'stage_description': '银白毛纹带冷焰边缘，攻击兼具冻结与灼烧的雏形效果。',
                'image_prompt': '幻想白虎幼体，银白毛纹，冰蓝与橙红双元素微光，高品质游戏立绘',
                'level_min': 1,
                'level_max': 9,
            },
            {
                'stage_index': 2,
                'stage_key': 'evolved',
                'stage_name': '烬霜战虎',
                'stage_description': '肩甲与护爪成形，双元素流体环绕，爆发与控制能力同步提升。',
                'image_prompt': '进化白虎战宠，冰火双元素流体，发光护甲，锐利爪刃，幻想战宠设定图',
                'level_min': 10,
                'level_max': 19,
            },
            {
                'stage_index': 3,
                'stage_key': 'ascended',
                'stage_name': '双极圣虎',
                'stage_description': '背部浮现冰焰圣环，怒吼可触发领域压制并重置元素循环。',
                'image_prompt': '超进化白虎，冰焰圣环，华丽重甲与符文，灵体粒子，史诗压迫感，传说皮肤风格',
                'level_min': 20,
                'level_max': 99,
            },
            {
                'stage_index': 4,
                'stage_key': 'ultimate',
                'stage_name': '极曜天虎机神',
                'stage_description': '虎躯披覆神机装甲，冰炎化为日蚀轮盘，具备终局统治力。',
                'image_prompt': '究极白虎机神，终极皮肤级别，日蚀轮盘，冰炎双核，华丽金属纹理与能量爆发，游戏立绘设定稿',
                'level_min': 100,
                'level_max': None,
            },
        ],
    },
    {
        'id': 9,
        'name': '曜金机甲狼',
        'pet_type': '灵能机械兽',
        'lore': '古代战争工坊遗留的自学习战狼核心，可根据战况重构外甲模块。',
        'rarity': '史诗',
        'image_url': None,
        'stages': [
            {
                'stage_index': 1,
                'stage_key': 'base',
                'stage_name': '启行狼核',
                'stage_description': '轻装骨架配备基础能量炉，具备高机动侦察与突袭能力。',
                'image_prompt': '幻想机械狼初始体，轻量外甲，金属青蓝发光核心，深色工业背景，游戏设定稿',
                'level_min': 1,
                'level_max': 9,
            },
            {
                'stage_index': 2,
                'stage_key': 'evolved',
                'stage_name': '裂光猎狼',
                'stage_description': '装甲模块扩展，背部能量刃翼展开，可执行高速切入打击。',
                'image_prompt': '进化机甲狼，裂光刃翼，青金能量纹路，机械细节丰富，战宠立绘，传说皮肤质感',
                'level_min': 10,
                'level_max': 19,
            },
            {
                'stage_index': 3,
                'stage_key': 'ascended',
                'stage_name': '恒曜战狼王',
                'stage_description': '核心炉升级为双环聚能，具备战场自修复与重火力模式。',
                'image_prompt': '超进化机械战狼王，双环聚能核心，华丽机甲重装，粒子尾焰，史诗级进化，游戏立绘',
                'level_min': 20,
                'level_max': 99,
            },
            {
                'stage_index': 4,
                'stage_key': 'ultimate',
                'stage_name': '神铸终端猎神',
                'stage_description': '全身转化为神铸级合金，狼首悬浮王印，进入绝对统御协议。',
                'image_prompt': '究极机甲狼神，终极形态，神铸合金与悬浮王印，复杂机械层次，顶级游戏皮肤设定图，强视觉冲击',
                'level_min': 100,
                'level_max': None,
            },
        ],
    },
    {
        'id': 10,
        'name': '天谕圣蛇',
        'pet_type': '神圣古灵',
        'lore': '古文明祭坛中苏醒的圣蛇契灵，以神谕铭文重塑战场秩序。',
        'rarity': '传说',
        'image_url': None,
        'stages': [
            {
                'stage_index': 1,
                'stage_key': 'base',
                'stage_name': '晨辉灵蛇',
                'stage_description': '鳞片映出柔和金辉，具备低阶净化与祝福加护能力。',
                'image_prompt': '幻想灵蛇初始形态，金白晨辉鳞片，神秘但克制，深色祭坛背景，高品质游戏立绘',
                'level_min': 1,
                'level_max': 9,
            },
            {
                'stage_index': 2,
                'stage_key': 'evolved',
                'stage_name': '圣纹耀蛇',
                'stage_description': '身躯浮现神谕纹章，可展开光幕净化并抵御负面状态。',
                'image_prompt': '进化圣蛇，神谕纹章，金色光幕，符文能量，幻想契约兽，高级游戏设定图',
                'level_min': 10,
                'level_max': 19,
            },
            {
                'stage_index': 3,
                'stage_key': 'ascended',
                'stage_name': '辉誓圣龙蛇',
                'stage_description': '头冠与翼膜化形，拥有圣域级群体增幅与裁定之力。',
                'image_prompt': '超进化圣龙蛇，华丽头冠翼膜，神圣符文矩阵，灵体粒子与光羽，史诗级进化，传说皮肤质感',
                'level_min': 20,
                'level_max': 99,
            },
            {
                'stage_index': 4,
                'stage_key': 'ultimate',
                'stage_name': '永昼神谕皇',
                'stage_description': '化作环天神蛇，铭文光环覆盖全场，具备终极祝福与审判双权。',
                'image_prompt': '究极圣蛇皇，终极皮肤级别，环天光环与神谕符文海，白金圣辉，史诗神殿场景，高级游戏立绘设定稿',
                'level_min': 100,
                'level_max': None,
            },
        ],
    },
]

for pet in PET_TEMPLATE_SEED:
    for stage in pet['stages']:
        stage['image_prompt'] = _expand_image_prompt(
            pet_name=pet['name'],
            pet_type=pet['pet_type'],
            rarity=pet['rarity'],
            stage_index=stage['stage_index'],
            stage_name=stage['stage_name'],
            stage_description=stage['stage_description'],
            core_prompt=stage['image_prompt'],
        )

