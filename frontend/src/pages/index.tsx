import React from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Wand2, Stars, Sparkles, Eye, Clock, Compass } from 'lucide-react';

const HomePage: React.FC = () => {
  const spreadTypes = [
    { 
      id: 'single',
      name: '单张牌占卜', 
      description: '快速获取每日指引或针对特定问题的简明答案，适合初学者和日常使用。', 
      icon: Sparkles,
      cards: 1,
      difficulty: '简单',
      usage: '日常指引、快速问答'
    },
    { 
      id: 'three_card',
      name: '三张牌占卜', 
      description: '洞察过去、现在与未来，理解事件的演变轨迹和时间脉络。', 
      icon: Clock,
      cards: 3,
      difficulty: '中等',
      usage: '时间线分析、情况发展'
    },
    { 
      id: 'celtic_cross',
      name: '凯尔特十字', 
      description: '全面剖析复杂问题，揭示深层影响与潜在结果，提供详细指导。', 
      icon: Compass,
      cards: 10,
      difficulty: '高级',
      usage: '复杂问题、深度分析'
    },
  ];

  const features = [
    {
      title: 'AI智能解读',
      description: '结合古老智慧与现代AI技术，为每张牌提供个性化深度解读',
      icon: Eye,
      color: 'from-purple-500 to-blue-500'
    },
    {
      title: '多种牌阵选择',
      description: '从简单的单张牌到复杂的凯尔特十字，满足不同需求',
      icon: Compass,
      color: 'from-amber-500 to-orange-500'
    },
    {
      title: '神秘视觉体验',
      description: '精美的塔罗牌视觉设计和流畅的交互动画效果',
      icon: Stars,
      color: 'from-pink-500 to-purple-500'
    }
  ];

  return (
    <>
      <Head>
        <title>神秘塔罗牌占卜师 - 探索内心深处的智慧</title>
        <meta name="description" content="专业的在线塔罗牌占卜，结合AI智能解读，为您的人生问题提供深刻洞察和指导" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen">
        {/* Hero Section */}
        <section className="hero-container">
          <div className="container-custom">
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, ease: "easeOut" }}
              className="text-center"
            >
              {/* Mystical Symbol */}
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
                className="inline-block mb-8"
              >
                <div className="w-24 h-24 md:w-32 md:h-32 mx-auto rounded-full bg-gradient-to-br from-purple-500 via-blue-600 to-purple-800 flex items-center justify-center shadow-2xl shadow-purple-500/30">
                  <Wand2 className="w-12 h-12 md:w-16 md:h-16 text-amber-300" />
                </div>
              </motion.div>

              {/* Hero Title */}
              <h1 className="hero-title font-mystical">
                神秘塔罗牌占卜师
              </h1>

              {/* Hero Subtitle */}
              <p className="hero-subtitle">
                探索内心深处的智慧与指引，让古老的塔罗牌为您的人生问题带来深刻洞察
              </p>

              {/* CTA Buttons */}
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.5 }}
                className="flex flex-col sm:flex-row gap-6 justify-center items-center"
              >
                <Link href="/reading">
                  <motion.button
                    whileHover={{ scale: 1.05, y: -3 }}
                    whileTap={{ scale: 0.95 }}
                    className="btn-primary flex items-center gap-3"
                  >
                    <Wand2 className="w-6 h-6" />
                    开始神秘占卜
                  </motion.button>
                </Link>

                <Link href="/learn">
                  <motion.button
                    whileHover={{ scale: 1.05, y: -3 }}
                    whileTap={{ scale: 0.95 }}
                    className="btn-secondary flex items-center gap-3"
                  >
                    <Stars className="w-6 h-6" />
                    学习塔罗奥秘
                  </motion.button>
                </Link>
              </motion.div>
            </motion.div>
          </div>
        </section>

        {/* SpreadSelector Section */}
        <section className="py-20 lg:py-32 relative">
          <div className="container-custom">
            {/* Section Header */}
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-responsive-lg font-mystical font-bold mb-6 text-gradient">
                选择您的神谕方式
              </h2>
              <div className="mystical-divider max-w-32 mx-auto"></div>
              <p className="text-responsive-base text-gray-300 max-w-3xl mx-auto mt-6">
                每种牌阵都承载着古老的智慧，选择最适合您问题的占卜方式
              </p>
            </motion.div>

            {/* Spread Cards Grid */}
            <div className="grid-responsive">
              {spreadTypes.map((spread, index) => (
                <Link key={spread.id} href="/reading">
                  <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.2 }}
                    viewport={{ once: true }}
                    className="spread-card group text-center h-full"
                  >
                    {/* Icon */}
                    <div className="mb-6">
                      <div className="w-20 h-20 mx-auto rounded-full bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center shadow-lg group-hover:shadow-amber-500/30 transition-all duration-300">
                        <spread.icon className="w-10 h-10 text-amber-300" />
                      </div>
                    </div>

                    {/* Title */}
                    <h3 className="text-2xl font-mystical font-bold mb-4 text-white group-hover:text-amber-300 transition-colors">
                      {spread.name}
                    </h3>

                    {/* Description */}
                    <p className="text-gray-300 mb-6 leading-relaxed">
                      {spread.description}
                    </p>

                    {/* Details */}
                    <div className="space-y-3">
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-purple-300">牌数:</span>
                        <span className="font-semibold text-amber-300">{spread.cards} 张</span>
                      </div>
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-purple-300">难度:</span>
                        <span className="font-semibold text-white">{spread.difficulty}</span>
                      </div>
                      <div className="text-xs text-gray-400 mt-4">
                        适用: {spread.usage}
                      </div>
                    </div>

                    {/* Hover indicator */}
                    <div className="mt-6 opacity-0 group-hover:opacity-100 transition-opacity text-sm text-amber-300">
                      点击开始占卜 →
                    </div>
                  </motion.div>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 lg:py-32 relative">
          <div className="absolute inset-0 bg-gradient-to-br from-purple-900/10 to-blue-900/10"></div>
          <div className="container-custom relative">
            {/* Section Header */}
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-responsive-lg font-mystical font-bold mb-6 text-gradient">
                神谕师的特殊能力
              </h2>
              <div className="mystical-divider max-w-32 mx-auto"></div>
              <p className="text-responsive-base text-gray-300 max-w-3xl mx-auto mt-6">
                融合古老智慧与现代科技，为您打开通往未知的神秘之门
              </p>
            </motion.div>

            {/* Features Grid */}
            <div className="grid-responsive">
              {features.map((feature, index) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.6, delay: index * 0.2 }}
                  viewport={{ once: true }}
                  className="text-center"
                >
                  <div className={`w-24 h-24 mx-auto rounded-full bg-gradient-to-br ${feature.color} flex items-center justify-center shadow-2xl mb-6`}>
                    <feature.icon className="w-12 h-12 text-white" />
                  </div>
                  
                  <h3 className="text-xl font-mystical font-bold mb-4 text-white">
                    {feature.title}
                  </h3>
                  
                  <p className="text-gray-300 leading-relaxed">
                    {feature.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Final CTA Section */}
        <section className="py-20 lg:py-32">
          <div className="container-narrow">
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="reading-card text-center"
            >
              <h2 className="text-responsive-lg font-mystical font-bold mb-6 text-gradient">
                准备好开始您的塔罗之旅了吗？
              </h2>
              
              <p className="text-responsive-base text-gray-300 mb-12 leading-relaxed">
                让神秘的塔罗牌为您揭示命运的指引，探索内心深处的智慧
              </p>
              
              <Link href="/reading">
                <motion.button
                  whileHover={{ scale: 1.05, y: -3 }}
                  whileTap={{ scale: 0.95 }}
                  className="btn-primary flex items-center gap-3 mx-auto text-xl px-12 py-5"
                >
                  <Wand2 className="w-6 h-6" />
                  立即开始占卜
                </motion.button>
              </Link>
            </motion.div>
          </div>
        </section>
      </main>
    </>
  );
};

export default HomePage;