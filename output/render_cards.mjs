import { chromium } from 'playwright';
import { mkdirSync, writeFileSync, existsSync, readFileSync } from 'fs';
import { execSync } from 'child_process';

const OUTPUT_DIR = '/Users/myke/Documents/MERJIC/概念库/output/cards';
const FONT_DIR = `${OUTPUT_DIR}/fonts`;

mkdirSync(OUTPUT_DIR, { recursive: true });

// Load fonts as base64
function fontToBase64(path) {
  return readFileSync(path).toString('base64');
}

const FONT_CSS = `
@font-face {
  font-family: 'Cormorant Garamond';
  font-style: normal;
  font-weight: 400;
  src: url(data:font/truetype;base64,${fontToBase64(`${FONT_DIR}/CormorantGaramond-Regular.ttf`)}) format('truetype');
}
@font-face {
  font-family: 'Cormorant Garamond';
  font-style: normal;
  font-weight: 500;
  src: url(data:font/truetype;base64,${fontToBase64(`${FONT_DIR}/CormorantGaramond-Medium.ttf`)}) format('truetype');
}
@font-face {
  font-family: 'Cormorant Garamond';
  font-style: normal;
  font-weight: 600;
  src: url(data:font/truetype;base64,${fontToBase64(`${FONT_DIR}/CormorantGaramond-SemiBold.ttf`)}) format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  src: url(data:font/truetype;base64,${fontToBase64(`${FONT_DIR}/Inter-Regular.ttf`)}) format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  src: url(data:font/truetype;base64,${fontToBase64(`${FONT_DIR}/Inter-Medium.ttf`)}) format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  src: url(data:font/truetype;base64,${fontToBase64(`${FONT_DIR}/Inter-SemiBold.ttf`)}) format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  src: url(data:font/truetype;base64,${fontToBase64(`${FONT_DIR}/Inter-Bold.ttf`)}) format('truetype');
}
`;

// 3:4 ratio, high quality for print
const CARD_W = 1080;
const CARD_H = 1440;
const SCALE = 2; // 2x for retina = 2160x2880 actual pixels

// Claude Design System tokens
const C = {
  primary: '#cc785c',
  primaryActive: '#a9583e',
  primaryDisabled: '#e6dfd8',
  ink: '#141413',
  body: '#3d3d3a',
  bodyStrong: '#252523',
  muted: '#6c6a64',
  mutedSoft: '#8e8b82',
  hairline: '#e6dfd8',
  hairlineSoft: '#ebe6df',
  canvas: '#faf9f5',
  surfaceSoft: '#f5f0e8',
  surfaceCard: '#efe9de',
  surfaceCreamStrong: '#e8e0d2',
  surfaceDark: '#181715',
  surfaceDarkElevated: '#252320',
  surfaceDarkSoft: '#1f1e1b',
  onPrimary: '#ffffff',
  onDark: '#faf9f5',
  onDarkSoft: '#a09d96',
  accentTeal: '#5db8a6',
  accentAmber: '#e8a55a',
  success: '#5db872',
  warning: '#d4a017',
  error: '#c64545',
};

const cards = [
  // 1. 封面
  {
    bg: C.surfaceDark,
    fg: C.onDark,
    accent: C.primary,
    content: `
      <div style="text-align:center; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; padding: 80px 72px;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; font-weight: 500; letter-spacing: 3px; color: ${C.onDarkSoft}; text-transform: uppercase; margin-bottom: 48px;">Roundtable</div>
        <h1 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 72px; font-weight: 400; line-height: 1.08; letter-spacing: -2px; color: ${C.onDark}; margin: 0 0 40px 0;">个体权力的<br>本质</h1>
        <div style="width: 48px; height: 3px; background: ${C.primary}; border-radius: 2px; margin-bottom: 40px;"></div>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; color: ${C.onDarkSoft}; line-height: 1.7; max-width: 520px; margin: 0 0 60px 0;">
          五位思想家——韦伯、尼采、赫拉利、纳瓦尔、森——<br>跨越社会学、哲学、历史学、科技投资与经济学，<br>就「个体权力的本质」展开四轮交锋。
        </p>
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.mutedSoft}; letter-spacing: 1px;">共 18 张 · MERJIC · 2026</div>
      </div>
    `,
  },
  // 2. 定义锚点
  {
    bg: C.canvas,
    fg: C.ink,
    accent: C.primary,
    content: `
      <div style="padding: 96px 80px;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.primary}; text-transform: uppercase; margin-bottom: 20px;">Definition</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 44px; font-weight: 400; line-height: 1.12; letter-spacing: -1px; color: ${C.ink}; margin: 0 0 48px 0;">统一定义</h2>
        <div style="background: ${C.surfaceCard}; border-radius: 12px; padding: 48px 40px; margin-bottom: 48px;">
          <p style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 26px; font-weight: 400; line-height: 1.45; color: ${C.bodyStrong}; margin: 0;">
            「个体权力 = 一个体在社会关系中，能够按照自身意志改变他人行为或结果的能力。」
          </p>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
          <div style="background: ${C.surfaceSoft}; border-radius: 8px; padding: 28px 24px;">
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; color: ${C.muted}; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px;">保留的模糊地带</div>
            <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.body}; line-height: 1.6; margin: 0;">「能力」是属性还是关系？「改变他人行为」是结果还是过程？</p>
          </div>
          <div style="background: ${C.surfaceSoft}; border-radius: 8px; padding: 28px 24px;">
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; color: ${C.muted}; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px;">讨论规则</div>
            <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.body}; line-height: 1.6; margin: 0;">以此为锚点，也以此为靶子——接受、修正、或拒绝。</p>
          </div>
        </div>
      </div>
    `,
  },
  // 3. 韦伯
  {
    bg: C.canvas,
    fg: C.ink,
    accent: C.primary,
    content: `
      <div style="padding: 96px 80px; display: flex; flex-direction: column; justify-content: center; height: 100%; box-sizing: border-box;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.accentAmber}; text-transform: uppercase; margin-bottom: 16px;">Max Weber · 社会学</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 48px; font-weight: 400; line-height: 1.1; letter-spacing: -1px; color: ${C.ink}; margin: 0 0 40px 0;">权力是关系中的<br>概率</h2>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; color: ${C.body}; line-height: 1.75; margin: 0 0 40px 0;">
          权力不是个人携带的某种资产——像口袋里的钥匙。它是「在某种社会关系内部，一个人的意志即使遇到抵抗也能贯彻的概率」。
        </p>
        <div style="border-left: 3px solid ${C.primary}; padding-left: 24px; margin-bottom: 40px;">
          <p style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 22px; color: ${C.bodyStrong}; line-height: 1.5; margin: 0;">
            同一个 CEO，在董事会上权力很高，在家里的餐桌上可能很低。离开了具体的社会关系，讨论个体权力毫无意义。
          </p>
        </div>
        <div style="background: ${C.surfaceCard}; border-radius: 8px; padding: 20px 24px; display: inline-block; align-self: flex-start;">
          <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; font-weight: 500; color: ${C.ink}; margin: 0;">关键词：概率 · 社会关系 · 非资产</p>
        </div>
      </div>
    `,
  },
  // 4. 尼采
  {
    bg: C.surfaceDark,
    fg: C.onDark,
    accent: C.primary,
    content: `
      <div style="padding: 96px 80px; display: flex; flex-direction: column; justify-content: center; height: 100%; box-sizing: border-box;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.primary}; text-transform: uppercase; margin-bottom: 16px;">Friedrich Nietzsche · 哲学</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 48px; font-weight: 400; line-height: 1.1; letter-spacing: -1px; color: ${C.onDark}; margin: 0 0 40px 0;">人本身就是<br>权力意志的具现</h2>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; color: ${C.onDarkSoft}; line-height: 1.75; margin: 0 0 40px 0;">
          权力意志（Wille zur Macht）是生命本身的根本冲动。每一种活着的事物都在努力扩展自身的力量、克服阻力、向外伸展。这是本体论事实，不是概率问题。
        </p>
        <div style="border-left: 3px solid ${C.primary}; padding-left: 24px; margin-bottom: 40px;">
          <p style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 22px; color: ${C.onDark}; line-height: 1.5; margin: 0;">
            人不是「拥有」权力，人就是权力的流动形式。个体本身就是权力意志的具现。
          </p>
        </div>
        <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 20px 24px; display: inline-block; align-self: flex-start;">
          <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; font-weight: 500; color: ${C.onDark}; margin: 0;">关键词：权力意志 · 本体论 · 生命冲动</p>
        </div>
      </div>
    `,
  },
  // 5. 赫拉利
  {
    bg: C.canvas,
    fg: C.ink,
    accent: C.primary,
    content: `
      <div style="padding: 96px 80px; display: flex; flex-direction: column; justify-content: center; height: 100%; box-sizing: border-box;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.accentTeal}; text-transform: uppercase; margin-bottom: 16px;">Yuval Noah Harari · 历史学</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 44px; font-weight: 400; line-height: 1.12; letter-spacing: -1px; color: ${C.ink}; margin: 0 0 40px 0;">权力来自<br>共同虚构的叙事</h2>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; color: ${C.body}; line-height: 1.75; margin: 0 0 36px 0;">
          智人统治地球靠的不是个体层面的力量——我们跑不过猎豹、打不过猩猩——靠的是共同虚构。国家、货币、法律、公司，只存在于集体想象中。
        </p>
        <div style="border-left: 3px solid ${C.accentTeal}; padding-left: 24px; margin-bottom: 36px;">
          <p style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 22px; color: ${C.bodyStrong}; line-height: 1.5; margin: 0;">
            如果明天所有人都停止相信「公司」这个概念，CEO 立刻失去一切权力。
          </p>
        </div>
        <div style="background: ${C.surfaceCard}; border-radius: 8px; padding: 20px 24px; display: inline-block; align-self: flex-start;">
          <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; font-weight: 500; color: ${C.ink}; margin: 0;">关键词：共同虚构 · 叙事掌控 · 集体信念</p>
        </div>
      </div>
    `,
  },
  // 6. 纳瓦尔
  {
    bg: C.surfaceDark,
    fg: C.onDark,
    accent: C.primary,
    content: `
      <div style="padding: 96px 80px; display: flex; flex-direction: column; justify-content: center; height: 100%; box-sizing: border-box;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.accentAmber}; text-transform: uppercase; margin-bottom: 16px;">Naval Ravikant · 科技投资</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 44px; font-weight: 400; line-height: 1.12; letter-spacing: -1px; color: ${C.onDark}; margin: 0 0 36px 0;">权力是杠杆</h2>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; color: ${C.onDarkSoft}; line-height: 1.75; margin: 0 0 32px 0;">
          一个人在社会中的权力，取决于他掌握的杠杆种类和量级。杠杆有四种，逐级递增——
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 32px;">
          <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 20px 24px;">
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: ${C.onDark}; margin-bottom: 4px;">1. 劳动力</div>
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft};">让人为你工作</div>
          </div>
          <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 20px 24px;">
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: ${C.onDark}; margin-bottom: 4px;">2. 资本</div>
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft};">用钱生钱</div>
          </div>
          <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 20px 24px; border: 1px solid ${C.accentAmber};">
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: ${C.accentAmber}; margin-bottom: 4px;">3. 代码 / 媒体</div>
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft};">无限复制，边际成本为零</div>
          </div>
          <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 20px 24px; border: 1px solid ${C.accentAmber};">
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: ${C.accentAmber}; margin-bottom: 4px;">4. AI</div>
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft};">放大决策能力</div>
          </div>
        </div>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.accentAmber}; font-weight: 500; margin: 0;">无需许可的杠杆 = 个人权力的倍增器</p>
      </div>
    `,
  },
  // 7. 森
  {
    bg: C.canvas,
    fg: C.ink,
    accent: C.primary,
    content: `
      <div style="padding: 96px 80px; display: flex; flex-direction: column; justify-content: center; height: 100%; box-sizing: border-box;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.accentTeal}; text-transform: uppercase; margin-bottom: 16px;">Amartya Sen · 经济学 / 哲学</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 44px; font-weight: 400; line-height: 1.12; letter-spacing: -1px; color: ${C.ink}; margin: 0 0 40px 0;">权力是可行能力</h2>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; color: ${C.body}; line-height: 1.75; margin: 0 0 36px 0;">
          你们都在讨论权力的「来源」——权力从哪里来，却没人问一个更根本的问题：<strong style="color: ${C.bodyStrong};">权力是为了什么？</strong>
        </p>
        <div style="border-left: 3px solid ${C.accentTeal}; padding-left: 24px; margin-bottom: 36px;">
          <p style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 22px; color: ${C.bodyStrong}; line-height: 1.5; margin: 0;">
            一个人能选择的实质自由的范围，才是他真正拥有的权力。
          </p>
        </div>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 15px; color: ${C.body}; line-height: 1.7; margin: 0;">
          你们把权力理解为「向外施加影响的能力」。我把权力理解为「向内实现自我的自由」。这是两个完全不同的方向。
        </p>
      </div>
    `,
  },
  // 8. 第一轮综述
  {
    bg: C.surfaceDark,
    fg: C.onDark,
    accent: C.primary,
    content: `
      <div style="padding: 88px 80px;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.primary}; text-transform: uppercase; margin-bottom: 16px;">Round 1 · 主持人综述</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 40px; font-weight: 400; line-height: 1.12; letter-spacing: -0.8px; color: ${C.onDark}; margin: 0 0 40px 0;">结构性分歧<br><span style="color: ${C.primary};">向外</span> vs <span style="color: ${C.accentTeal};">向内</span></h2>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 32px;">
          <div>
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: ${C.primary}; margin-bottom: 14px; letter-spacing: 0.5px;">向外阵营 · 权力 = 对他者的作用力</div>
            <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 16px 20px; margin-bottom: 8px;">
              <span style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft};">尼采</span>
              <span style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.mutedSoft}; margin-left: 8px;">本体论 — 生命冲动</span>
            </div>
            <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 16px 20px; margin-bottom: 8px;">
              <span style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft};">韦伯</span>
              <span style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.mutedSoft}; margin-left: 8px;">关系层 — 关系中的概率</span>
            </div>
            <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 16px 20px; margin-bottom: 8px;">
              <span style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft};">赫拉利</span>
              <span style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.mutedSoft}; margin-left: 8px;">认知层 — 共同叙事</span>
            </div>
            <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 16px 20px;">
              <span style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft};">纳瓦尔</span>
              <span style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.mutedSoft}; margin-left: 8px;">工具层 — 杠杆</span>
            </div>
          </div>
          <div>
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: ${C.accentTeal}; margin-bottom: 14px; letter-spacing: 0.5px;">向内阵营 · 权力 = 对自身生活的掌控</div>
            <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 16px 20px; margin-bottom: 8px;">
              <span style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft};">森</span>
              <span style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.mutedSoft}; margin-left: 8px;">规范层 — 可行能力 / 实质自由</span>
            </div>
            <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 16px 20px; margin-top: 48px;">
              <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft}; line-height: 1.6; margin: 0;">
                最大裂缝：<br>尼采说权力<strong style="color: ${C.onDark};">先于社会</strong>，<br>赫拉利说权力<strong style="color: ${C.onDark};">社会建构</strong>。
              </p>
            </div>
          </div>
        </div>
      </div>
    `,
  },
  // 9. 第二轮引导
  {
    bg: C.canvas,
    fg: C.ink,
    accent: C.primary,
    content: `
      <div style="padding: 96px 80px; display: flex; flex-direction: column; justify-content: center; height: 100%; box-sizing: border-box;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.primary}; text-transform: uppercase; margin-bottom: 16px;">Round 2 · 引导问题</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 40px; font-weight: 400; line-height: 1.12; letter-spacing: -0.8px; color: ${C.ink}; margin: 0 0 48px 0;">冲动如何变成<br>被承认的力量？</h2>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; color: ${C.body}; line-height: 1.8; margin: 0 0 48px 0;">
          尼采说权力冲动在先，赫拉利说社会认可在后。那两者之间的接口是什么——是什么机制把一个「想要」变成了一种「被承认的力量」？
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
          <div style="border: 1px solid ${C.hairline}; border-radius: 8px; padding: 24px;">
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; font-weight: 500; color: ${C.ink}; margin-bottom: 6px;">权力意志</div>
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.muted};">（尼采：想要）</div>
          </div>
          <div style="display: flex; align-items: center; justify-content: center;">
            <div style="background: ${C.primary}; border-radius: 9999px; padding: 10px 20px;">
              <span style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; font-weight: 500; color: ${C.onPrimary};">接口 = ？</span>
            </div>
          </div>
        </div>
        <div style="margin-top: 24px; border: 1px solid ${C.hairline}; border-radius: 8px; padding: 24px;">
          <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; font-weight: 500; color: ${C.ink}; margin-bottom: 6px;">被承认的力量</div>
          <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.muted};">（赫拉利：社会认可）</div>
        </div>
      </div>
    `,
  },
  // 10. 韦伯的合法性三阶
  {
    bg: C.surfaceDark,
    fg: C.onDark,
    accent: C.primary,
    content: `
      <div style="padding: 88px 80px;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.accentAmber}; text-transform: uppercase; margin-bottom: 16px;">Weber · 合法性三阶</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 40px; font-weight: 400; line-height: 1.12; letter-spacing: -0.8px; color: ${C.onDark}; margin: 0 0 40px 0;">合法化过程</h2>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 15px; color: ${C.onDarkSoft}; line-height: 1.7; margin: 0 0 36px 0;">
          冲动要变成权力，中间必须经过一道关卡：他人承认你有权这样做。
        </p>
        <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 40px;">
          <div style="display: flex; align-items: flex-start; gap: 20px;">
            <div style="min-width: 40px; height: 40px; background: ${C.accentAmber}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; font-weight: 600; color: ${C.surfaceDark};">1</div>
            <div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; font-weight: 500; color: ${C.onDark}; margin-bottom: 4px;">传统型</div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.onDarkSoft}; line-height: 1.5;">「一直都是这样的」— 权威来自惯例</div>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 20px;">
            <div style="min-width: 40px; height: 40px; background: ${C.accentAmber}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; font-weight: 600; color: ${C.surfaceDark};">2</div>
            <div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; font-weight: 500; color: ${C.onDark}; margin-bottom: 4px;">魅力型</div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.onDarkSoft}; line-height: 1.5;">「这个人本身非凡」— 权威来自个人品质</div>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 20px;">
            <div style="min-width: 40px; height: 40px; background: ${C.accentAmber}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; font-weight: 600; color: ${C.surfaceDark};">3</div>
            <div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; font-weight: 500; color: ${C.onDark}; margin-bottom: 4px;">法理型</div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.onDarkSoft}; line-height: 1.5;">「规则赋予了这个职位」— 权威来自制度框架</div>
            </div>
          </div>
        </div>
        <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 16px 20px;">
          <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft}; line-height: 1.5; margin: 0;">
            权力意志 → 寻求他人承认 → 基于正当性逻辑给予承认 → 权力成立。<br><strong style="color: ${C.onDark};">这个过程是动态的、可逆的。</strong>
          </p>
        </div>
      </div>
    `,
  },
  // 11. Naval 的无许可杠杆
  {
    bg: C.canvas,
    fg: C.ink,
    accent: C.primary,
    content: `
      <div style="padding: 88px 80px;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.accentAmber}; text-transform: uppercase; margin-bottom: 16px;">Naval · 无需许可的世界</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 40px; font-weight: 400; line-height: 1.12; letter-spacing: -0.8px; color: ${C.ink}; margin: 0 0 36px 0;">创造物的传播<br>本身就是权力</h2>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; color: ${C.body}; line-height: 1.75; margin: 0 0 32px 0;">
          一个没有任何「合法性」的人，写了一段代码开源出去，被一百万人使用。他不认识这些人，这些人也没有「承认」他有权做什么。但他事实上拥有了巨大的影响力。
        </p>
        <div style="background: ${C.surfaceCard}; border-radius: 12px; padding: 32px 28px; margin-bottom: 28px;">
          <p style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 20px; color: ${C.bodyStrong}; line-height: 1.5; margin: 0;">
            在代码和媒体的世界里，创造物本身就是权力，不需要任何人的承认。
          </p>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
          <div style="background: ${C.surfaceSoft}; border-radius: 8px; padding: 20px;">
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: ${C.muted}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">Permissioned</div>
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.body};">劳动力 · 资本<br>需要别人许可</div>
          </div>
          <div style="background: ${C.surfaceCard}; border: 1px solid ${C.accentAmber}; border-radius: 8px; padding: 20px;">
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: ${C.accentAmber}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">Permissionless</div>
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.bodyStrong};">代码 · 媒体 · AI<br>无需任何人批准</div>
          </div>
        </div>
      </div>
    `,
  },
  // 12. 尼采的反击
  {
    bg: C.surfaceDark,
    fg: C.onDark,
    accent: C.primary,
    content: `
      <div style="padding: 96px 80px; display: flex; flex-direction: column; justify-content: center; height: 100%; box-sizing: border-box;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.primary}; text-transform: uppercase; margin-bottom: 16px;">Nietzsche · 反击</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 42px; font-weight: 400; line-height: 1.1; letter-spacing: -0.8px; color: ${C.onDark}; margin: 0 0 36px 0;">价值创造先行<br>合法性事后追认</h2>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; color: ${C.onDarkSoft}; line-height: 1.75; margin: 0 0 36px 0;">
          Naval 描述的现象恰恰印证了我的观点。一个程序员花无数个小时写代码——这种「想要创造」的冲动从何而来？正是权力意志。
        </p>
        <div style="border-left: 3px solid ${C.primary}; padding-left: 24px; margin-bottom: 36px;">
          <p style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 22px; color: ${C.onDark}; line-height: 1.5; margin: 0;">
            权力意志驱动了价值创造，然后社会才追认这种创造为「合法的权力」。顺序不能反。
          </p>
        </div>
        <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 24px;">
          <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.onDarkSoft}; line-height: 1.6; margin: 0;">
            韦伯说的「合法性」——那只是权力意志被<strong style="color: ${C.onDark};">群畜道德</strong>驯化后的产物。弱者为了限制强者的权力意志，发明了「合法性」这套话语：你不能直接行使力量，你必须先获得「承认」。
          </p>
        </div>
      </div>
    `,
  },
  // 13. 赫拉利的回应：叙事地基
  {
    bg: C.canvas,
    fg: C.ink,
    accent: C.accentTeal,
    content: `
      <div style="padding: 88px 80px;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.accentTeal}; text-transform: uppercase; margin-bottom: 16px;">Harari · 三步机制</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 38px; font-weight: 400; line-height: 1.12; letter-spacing: -0.8px; color: ${C.ink}; margin: 0 0 36px 0;">没有任何权力<br>能脱离共同信念运作</h2>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 15px; color: ${C.body}; line-height: 1.7; margin: 0 0 32px 0;">
          看似「无需许可」的杠杆，其实站在深层的叙事地基上。
        </p>
        <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 36px;">
          <div style="display: flex; align-items: flex-start; gap: 20px;">
            <div style="min-width: 40px; height: 40px; background: ${C.accentTeal}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; font-weight: 600; color: ${C.canvas};">1</div>
            <div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; font-weight: 500; color: ${C.ink}; margin-bottom: 4px;">叙事植入</div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.body}; line-height: 1.5;">一个故事被注入集体意识</div>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 20px;">
            <div style="min-width: 40px; height: 40px; background: ${C.accentTeal}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; font-weight: 600; color: ${C.canvas};">2</div>
            <div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; font-weight: 500; color: ${C.ink}; margin-bottom: 4px;">制度固化</div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.body}; line-height: 1.5;">叙事被写入法律、规范、市场机制</div>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 20px;">
            <div style="min-width: 40px; height: 40px; background: ${C.accentTeal}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; font-weight: 600; color: ${C.canvas};">3</div>
            <div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; font-weight: 500; color: ${C.ink}; margin-bottom: 4px;">行为协调</div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.body}; line-height: 1.5;">大量个体基于信任而协调行动</div>
            </div>
          </div>
        </div>
        <div style="background: ${C.surfaceCard}; border-radius: 8px; padding: 20px 24px;">
          <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.body}; line-height: 1.6; margin: 0;">
            开源程序员权力看似不需要「承认」，但依赖巨大的叙事基础设施：互联网协议、开源运动、编程语言——没有这些前置集体信念，代码只是无意义的字符。
          </p>
        </div>
      </div>
    `,
  },
  // 14. 森的质问
  {
    bg: C.primary,
    fg: C.onPrimary,
    accent: C.onPrimary,
    content: `
      <div style="padding: 96px 80px; display: flex; flex-direction: column; justify-content: center; height: 100%; box-sizing: border-box;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: rgba(255,255,255,0.7); text-transform: uppercase; margin-bottom: 16px;">Sen · 质问</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 44px; font-weight: 400; line-height: 1.1; letter-spacing: -1px; color: ${C.onPrimary}; margin: 0 0 40px 0;">你们讨论的权力<br>是掌权者的自我理解</h2>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 16px; color: rgba(255,255,255,0.85); line-height: 1.75; margin: 0 0 32px 0;">
          这整个框架都在预设权力的主体是一个「想要影响他人」的行动者。但现实中有大量人——可能是这个世界上大多数的人——他们并不「想要」影响他人。
        </p>
        <div style="border-left: 3px solid rgba(255,255,255,0.5); padding-left: 24px; margin-bottom: 36px;">
          <p style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 22px; color: ${C.onPrimary}; line-height: 1.5; margin: 0;">
            韦伯谈合法性——但无权者连进入这个框架的资格都没有。Naval 谈杠杆——但拥有杠杆的前提是有资本、有教育、有时间。
          </p>
        </div>
        <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 15px; color: rgba(255,255,255,0.8); line-height: 1.7; margin: 0;">
          大多数人的权力问题不是「如何影响他人」，而是「如何拥有选择自己生活的自由」。
        </p>
      </div>
    `,
  },
  // 15. 第三轮：自由与权力
  {
    bg: C.surfaceDark,
    fg: C.onDark,
    accent: C.primary,
    content: `
      <div style="padding: 88px 80px;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.primary}; text-transform: uppercase; margin-bottom: 16px;">Round 3 · 自由与权力的关系</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 36px; font-weight: 400; line-height: 1.12; letter-spacing: -0.8px; color: ${C.onDark}; margin: 0 0 32px 0;">自由与权力<br>可分吗？</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 28px;">
          <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 18px 20px;">
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: ${C.accentAmber}; font-weight: 500; margin-bottom: 8px;">可分派 · Naval</div>
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft}; line-height: 1.5;">自由是你自己的事，权力是别人的事。独居农夫有自由无权力。</div>
          </div>
          <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 18px 20px;">
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: ${C.accentTeal}; font-weight: 500; margin-bottom: 8px;">条件派 · 韦伯</div>
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft}; line-height: 1.5;">自由是权力的必要不充分条件。两者条件相关但方向不同。</div>
          </div>
          <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 18px 20px;">
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: ${C.primary}; font-weight: 500; margin-bottom: 8px;">同一派 · Harari</div>
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft}; line-height: 1.5;">「选择自由」本身就是叙事建构的。你一旦选择了，就已经在影响他人。</div>
          </div>
          <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 18px 20px;">
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: ${C.mutedSoft}; font-weight: 500; margin-bottom: 8px;">还原派 · 尼采</div>
            <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.onDarkSoft}; line-height: 1.5;">都是权力意志的表现。所谓可分只是分析框架的切割，不是本体论事实。</div>
          </div>
        </div>
        <div style="background: ${C.primary}; border-radius: 8px; padding: 20px 24px;">
          <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: rgba(255,255,255,0.7); font-weight: 500; margin-bottom: 8px;">基础派 · 森</div>
          <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; color: ${C.onPrimary}; line-height: 1.5;">经验上可分，但规范上不应分开。影响他人的能力是表层现象，可行能力是深层基础。社会应该关注根基。</div>
        </div>
      </div>
    `,
  },
  // 16. 第四轮：五条核心定义
  {
    bg: C.canvas,
    fg: C.ink,
    accent: C.primary,
    content: `
      <div style="padding: 80px 72px;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.primary}; text-transform: uppercase; margin-bottom: 12px;">Round 4 · 收拢</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 36px; font-weight: 400; line-height: 1.12; letter-spacing: -0.8px; color: ${C.ink}; margin: 0 0 28px 0;">最朴素的那条</h2>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          <div style="display: flex; align-items: flex-start; gap: 16px; background: ${C.surfaceSoft}; border-radius: 8px; padding: 18px 20px;">
            <div style="min-width: 6px; height: 100%; min-height: 40px; background: ${C.accentAmber}; border-radius: 3px;"></div>
            <div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: ${C.accentAmber}; margin-bottom: 4px;">韦伯</div>
              <p style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 17px; color: ${C.bodyStrong}; line-height: 1.45; margin: 0;">权力的核心是他人听从你的理由。</p>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 16px; background: ${C.surfaceSoft}; border-radius: 8px; padding: 18px 20px;">
            <div style="min-width: 6px; height: 100%; min-height: 40px; background: ${C.primary}; border-radius: 3px;"></div>
            <div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: ${C.primary}; margin-bottom: 4px;">尼采</div>
              <p style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 17px; color: ${C.bodyStrong}; line-height: 1.45; margin: 0;">权力的核心是对自身生命力的扩展——克服阻碍，继续生长。</p>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 16px; background: ${C.surfaceSoft}; border-radius: 8px; padding: 18px 20px;">
            <div style="min-width: 6px; height: 100%; min-height: 40px; background: ${C.accentTeal}; border-radius: 3px;"></div>
            <div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: ${C.accentTeal}; margin-bottom: 4px;">赫拉利</div>
              <p style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 17px; color: ${C.bodyStrong}; line-height: 1.45; margin: 0;">权力的核心是制造共识——让他人相信你相信的东西。</p>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 16px; background: ${C.surfaceSoft}; border-radius: 8px; padding: 18px 20px;">
            <div style="min-width: 6px; height: 100%; min-height: 40px; background: ${C.accentAmber}; border-radius: 3px;"></div>
            <div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: ${C.accentAmber}; margin-bottom: 4px;">纳瓦尔</div>
              <p style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 17px; color: ${C.bodyStrong}; line-height: 1.45; margin: 0;">权力的核心是创造脱离肉身持续运作的东西——杠杆让意志自治。</p>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 16px; background: ${C.surfaceCard}; border: 1px solid ${C.hairline}; border-radius: 8px; padding: 18px 20px;">
            <div style="min-width: 6px; height: 100%; min-height: 40px; background: ${C.accentTeal}; border-radius: 3px;"></div>
            <div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; font-weight: 500; color: ${C.accentTeal}; margin-bottom: 4px;">森</div>
              <p style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 17px; color: ${C.bodyStrong}; line-height: 1.45; margin: 0;">权力的核心是选择空间不被他人压缩——首先是不被夺走，其次才是去扩张。</p>
            </div>
          </div>
        </div>
      </div>
    `,
  },
  // 17. 整合模型
  {
    bg: C.surfaceDark,
    fg: C.onDark,
    accent: C.primary,
    content: `
      <div style="padding: 72px 72px;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.primary}; text-transform: uppercase; margin-bottom: 10px;">整合共识</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 34px; font-weight: 400; line-height: 1.12; letter-spacing: -0.8px; color: ${C.onDark}; margin: 0 0 24px 0;">四层运作系统</h2>
        <div style="display: flex; flex-direction: column; gap: 0; margin-bottom: 24px;">
          <div style="background: ${C.primary}; border-radius: 8px; padding: 16px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div>
                <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 11px; color: rgba(255,255,255,0.6); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 3px;">第四层 · 尼采</div>
                <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; font-weight: 500; color: ${C.onPrimary};">生命力扩展</div>
              </div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: rgba(255,255,255,0.7);">权力的燃料</div>
            </div>
          </div>
          <div style="text-align: center; color: ${C.mutedSoft}; font-size: 16px; padding: 6px 0;">↓ 驱动</div>
          <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 16px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div>
                <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 11px; color: ${C.accentAmber}; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 3px;">第三层 · 纳瓦尔</div>
                <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; font-weight: 500; color: ${C.onDark};">杠杆构建</div>
              </div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: ${C.onDarkSoft};">权力的放大器</div>
            </div>
          </div>
          <div style="text-align: center; color: ${C.mutedSoft}; font-size: 16px; padding: 6px 0;">↓ 依托</div>
          <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 16px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div>
                <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 11px; color: ${C.accentTeal}; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 3px;">第二层 · 赫拉利</div>
                <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; font-weight: 500; color: ${C.onDark};">共识制造</div>
              </div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: ${C.onDarkSoft};">权力的社会粘合剂</div>
            </div>
          </div>
          <div style="text-align: center; color: ${C.mutedSoft}; font-size: 16px; padding: 6px 0;">↓ 表现为</div>
          <div style="background: ${C.surfaceDarkElevated}; border-radius: 8px; padding: 16px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div>
                <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 11px; color: ${C.accentAmber}; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 3px;">第一层 · 韦伯</div>
                <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; font-weight: 500; color: ${C.onDark};">让事情按你的方向走</div>
              </div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: ${C.onDarkSoft};">权力的可见输出</div>
            </div>
          </div>
          <div style="text-align: center; color: ${C.mutedSoft}; font-size: 16px; padding: 6px 0;">↓ 反过来要求</div>
          <div style="background: ${C.accentTeal}; border-radius: 8px; padding: 16px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div>
                <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 11px; color: rgba(255,255,255,0.6); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 3px;">基础层 · 森</div>
                <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 14px; font-weight: 500; color: ${C.onPrimary};">选择空间不被压缩</div>
              </div>
              <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: rgba(255,255,255,0.8);">权力的底线</div>
            </div>
          </div>
        </div>
      </div>
    `,
  },
  // 18. 开放问题 + 结尾
  {
    bg: C.canvas,
    fg: C.ink,
    accent: C.primary,
    content: `
      <div style="padding: 96px 80px; display: flex; flex-direction: column; justify-content: center; height: 100%; box-sizing: border-box;">
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 2px; color: ${C.muted}; text-transform: uppercase; margin-bottom: 20px;">Open Questions</div>
        <h2 style="font-family: 'Copernicus', 'Tiempos Headline', 'Cormorant Garamond', serif; font-size: 38px; font-weight: 400; line-height: 1.12; letter-spacing: -0.8px; color: ${C.ink}; margin: 0 0 40px 0;">未解决的<br>开放问题</h2>
        <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 48px;">
          <div style="display: flex; gap: 14px; align-items: flex-start;">
            <div style="min-width: 28px; height: 28px; border: 1.5px solid ${C.primary}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: ${C.primary}; font-weight: 500; margin-top: 2px;">1</div>
            <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 15px; color: ${C.body}; line-height: 1.6; margin: 0;">权力意志是否必须存在？森的可行能力框架能否完全独立于尼采的权力意志？</p>
          </div>
          <div style="display: flex; gap: 14px; align-items: flex-start;">
            <div style="min-width: 28px; height: 28px; border: 1.5px solid ${C.primary}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: ${C.primary}; font-weight: 500; margin-top: 2px;">2</div>
            <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 15px; color: ${C.body}; line-height: 1.6; margin: 0;">共识的黑暗面——当共识被恶意制造（操纵、洗脑、信息茧房），它还是权力的合法形式吗？</p>
          </div>
          <div style="display: flex; gap: 14px; align-items: flex-start;">
            <div style="min-width: 28px; height: 28px; border: 1.5px solid ${C.primary}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: ${C.primary}; font-weight: 500; margin-top: 2px;">3</div>
            <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 15px; color: ${C.body}; line-height: 1.6; margin: 0;">无许可杠杆正在被平台垄断——当杠杆本身被集中控制时，「无需许可」是否变成了幻觉？</p>
          </div>
          <div style="display: flex; gap: 14px; align-items: flex-start;">
            <div style="min-width: 28px; height: 28px; border: 1.5px solid ${C.primary}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'StyreneB', 'Inter', sans-serif; font-size: 12px; color: ${C.primary}; font-weight: 500; margin-top: 2px;">4</div>
            <p style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 15px; color: ${C.body}; line-height: 1.6; margin: 0;">底线由谁来守护？压缩他人选择空间的往往正是拥有最大权力的人。</p>
          </div>
        </div>
        <div style="width: 48px; height: 2px; background: ${C.hairline}; margin-bottom: 24px;"></div>
        <div style="font-family: 'StyreneB', 'Inter', sans-serif; font-size: 13px; color: ${C.mutedSoft}; letter-spacing: 1px;">MERJIC · Roundtable · 2026</div>
      </div>
    `,
  },
];

// Generate HTML for each card
function generateCardHTML(card, index) {
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  ${FONT_CSS}

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    width: ${CARD_W}px;
    height: ${CARD_H}px;
    overflow: hidden;
    background: ${card.bg};
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
</style>
</head>
<body>
${card.content}
</body>
</html>`;
}

// Main render function
async function main() {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: CARD_W, height: CARD_H },
    deviceScaleFactor: SCALE,
  });
  const page = await context.newPage();

  const pngPaths = [];

  for (let i = 0; i < cards.length; i++) {
    const html = generateCardHTML(cards[i], i);
    const htmlPath = `${OUTPUT_DIR}/card_${String(i + 1).padStart(2, '0')}.html`;
    writeFileSync(htmlPath, html);

    await page.setContent(html, { waitUntil: 'networkidle' });
    // Wait for fonts to load (base64 inline fonts need extra time)
    await page.waitForTimeout(3000);

    const pngPath = `${OUTPUT_DIR}/card_${String(i + 1).padStart(2, '0')}.png`;
    await page.screenshot({
      path: pngPath,
      type: 'png',
      clip: { x: 0, y: 0, width: CARD_W, height: CARD_H },
    });

    pngPaths.push(pngPath);
    console.log(`✓ Card ${i + 1}/${cards.length} rendered`);
  }

  await browser.close();

  // Build PDF using Python PIL
  console.log('\nBuilding PDF...');
  execSync(`python3 -c "
from PIL import Image
import os

output_dir = '${OUTPUT_DIR}'
png_files = sorted([f for f in os.listdir(output_dir) if f.endswith('.png') and f.startswith('card_')])
images = [Image.open(os.path.join(output_dir, f)) for f in png_files]

# Save as PDF
pdf_path = os.path.join(output_dir, '个体权力的本质_小红书卡片.pdf')
if images:
    images[0].save(pdf_path, 'PDF', save_all=True, append_images=images[1:], resolution=300)
    print(f'✓ PDF saved: {pdf_path}')

# Create ZIP
import zipfile
zip_path = os.path.join(output_dir, '个体权力的本质_小红书卡片.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in png_files:
        zf.write(os.path.join(output_dir, f), f)
print(f'✓ ZIP saved: {zip_path}')
print(f'Total cards: {len(png_files)}')
"`);

  // Cleanup HTML files
  for (let i = 0; i < cards.length; i++) {
    const htmlPath = `${OUTPUT_DIR}/card_${String(i + 1).padStart(2, '0')}.html`;
    if (existsSync(htmlPath)) {
      execSync(`rm "${htmlPath}"`);
    }
  }

  console.log('\nDone! Files in:', OUTPUT_DIR);
}

main().catch(err => {
  console.error('Render failed:', err);
  process.exit(1);
});
