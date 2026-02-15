# デブポジBot 有料化セットアップガイド

## 方法1: noteメンバーシップ（推奨・簡単）

noteのメンバーシップ機能を使って有料プランを提供。

### 手順
1. [note.com/coyass](https://note.com/coyass) にログイン
2. クリエイターページ → メンバーシップ → 作成
3. プランを作成:

#### プラン1: PREMIUM（¥500/月）
- **プラン名:** デブポジBot PREMIUM
- **説明:** AI搭載デブポジ変換、API利用（月1,000回）、自動リプライBot設定、カスタム応答、メンバー指名変換
- **特典記事:** PREMIUMメンバー限定のAPIキー発行手順

#### プラン2: PRO（¥2,000/月）
- **プラン名:** デブポジBot PRO
- **説明:** 全機能無制限、複数SNS自動Bot、企業利用OK、DEV PARADE公認バッジ、メンバーからDM
- **特典記事:** PRO限定のフル機能APIキー + メンバーとの直接やりとり

### 収益予測
- PREMIUM 100名 × ¥500 = ¥50,000/月
- PRO 20名 × ¥2,000 = ¥40,000/月
- **月間: ¥90,000** (note手数料前)

---

## 方法2: Stripe（高度・API連携可能）

Stripeを使って直接課金。APIキーの自動発行も可能。

### 手順

#### 1. Stripeアカウント作成
- https://dashboard.stripe.com/register
- 本人確認・銀行口座登録

#### 2. Stripe商品/価格作成
```bash
# Stripe CLIでプラン作成
stripe products create --name="DebuPosiBot PREMIUM" --description="AI搭載デブポジ変換 月1,000回API"
stripe prices create --product=prod_xxx --unit-amount=500 --currency=jpy --recurring[interval]=month

stripe products create --name="DebuPosiBot PRO" --description="全機能無制限 複数SNS自動Bot"
stripe prices create --product=prod_yyy --unit-amount=2000 --currency=jpy --recurring[interval]=month
```

#### 3. Checkout Session（決済ページ）
debu-bot.htmlのSUBSCRIBEボタンをStripe Checkoutにリンク。

#### 4. 必要なSecrets
リポジトリに追加:
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `STRIPE_PRICE_PREMIUM` (¥500プランのprice_id)
- `STRIPE_PRICE_PRO` (¥2,000プランのprice_id)

---

## 方法3: Stripe + GitHub Actions（自動API発行）

課金されたら自動でAPIキーを発行し、GitHub Issueで通知。

### フロー
1. ユーザーがStripe Checkoutで決済
2. Stripe Webhookがサーバーに通知
3. APIキーを自動生成
4. ユーザーにメールで通知
5. APIキーでデブポジBot APIを利用可能

※ この方式はVercel/Cloudflare Workers等のサーバーレス環境が必要

---

## おすすめ: noteメンバーシップ → Stripeへ段階移行

1. **まずnoteメンバーシップで開始**（設定が簡単、既存のnoteユーザーベースを活用）
2. **ユーザーが増えたらStripeに移行**（手数料が低い、API連携可能）
3. **最終的にはWebアプリ化**（Next.js + Stripe + Vercel）
