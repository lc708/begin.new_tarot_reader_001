import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowLeft, Search, BookOpen, Star, Crown, Sword, Heart, Diamond, Coins, Wand, Eye, Clock, Compass } from 'lucide-react';

const LearnPage: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<'all' | 'major_arcana' | 'minor_arcana'>('all');
  const [selectedCard, setSelectedCard] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  // 塔罗牌数据
  const majorArcana = [
    { id: 'fool', name: '愚者', number: 0, keywords: '新开始, 冒险, 纯真', description: '代表新的开始和无限的可能性，鼓励我们以开放的心态面对未知。' },
    { id: 'magician', name: '魔术师', number: 1, keywords: '意志力, 创造, 技能', description: '象征着将想法转化为现实的能力，提醒我们拥有改变生活的力量。' },
    { id: 'high_priestess', name: '女祭司', number: 2, keywords: '直觉, 神秘, 内在智慧', description: '代表内在的智慧和直觉，引导我们倾听内心的声音。' },
    { id: 'empress', name: '女皇', number: 3, keywords: '丰富, 创造力, 母性', description: '象征丰饶与创造力，代表生命的孕育和成长。' },
    { id: 'emperor', name: '皇帝', number: 4, keywords: '权威, 结构, 领导', description: '代表秩序与权威，强调建立稳固的基础和领导能力。' },
    { id: 'hierophant', name: '教皇', number: 5, keywords: '传统, 学习, 指导', description: '象征传统智慧和精神指导，提醒我们学习和传承的重要性。' }
  ];

  const minorArcana = [
    { suit: 'cups', name: '圣杯', icon: Heart, color: 'text-blue-400', description: '代表情感、爱情、人际关系和精神层面。' },
    { suit: 'wands', name: '权杖', icon: Wand, color: 'text-red-400', description: '象征激情、创造力、行动力和事业发展。' },
    { suit: 'swords', name: '宝剑', icon: Sword, color: 'text-gray-400', description: '代表思想、沟通、冲突和理性分析。' },
    { suit: 'pentacles', name: '星币', icon: Coins, color: 'text-yellow-400', description: '象征物质、金钱、健康和实用层面。' }
  ];

  const spreadGuides = [
    {
      id: 'single',
      name: '单张牌占卜',
      icon: Star,
      cards: 1,
      difficulty: '简单',
      layout: '●',
      description: '最简单的占卜方式，适合日常指引和快速问答。',
      positions: [
        { name: '当前状况', description: '针对问题的直接指导和建议' }
      ],
      usage: '适用于日常决策、情绪指导、每日灵感等简单问题。',
      tips: '专注于一个具体问题，让直觉引导你选择合适的牌。'
    },
    {
      id: 'three_card',
      name: '三张牌占卜',
      icon: Clock,
      cards: 3,
      difficulty: '中等',
      layout: '● ● ●',
      description: '经典的时间线占卜，揭示事件的发展轨迹。',
      positions: [
        { name: '过去', description: '影响当前情况的过去因素' },
        { name: '现在', description: '当前的状况和挑战' },
        { name: '未来', description: '可能的发展和结果' }
      ],
      usage: '适用于了解事件发展、关系进展、项目规划等需要时间维度的问题。',
      tips: '关注三张牌之间的联系，它们共同讲述了一个完整的故事。'
    },
    {
      id: 'celtic_cross',
      name: '凯尔特十字',
      icon: Compass,
      cards: 10,
      difficulty: '高级',
      layout: '复杂十字布局',
      description: '最全面的占卜牌阵，提供深度洞察和全方位分析。',
      positions: [
        { name: '当前状况', description: '问题的核心和当前状态' },
        { name: '挑战/机遇', description: '需要面对的挑战或可能的机遇' },
        { name: '遥远过去', description: '深层的根源和基础' },
        { name: '近期过去', description: '最近发生的相关事件' },
        { name: '可能未来', description: '如果保持现状的发展方向' },
        { name: '近期未来', description: '接下来会发生的事' },
        { name: '你的方法', description: '你处理问题的方式' },
        { name: '外部影响', description: '环境和他人的影响' },
        { name: '内心感受', description: '你的真实想法和感受' },
        { name: '最终结果', description: '问题的最终走向和结果' }
      ],
      usage: '适用于复杂的人生问题、重大决策、深度自我分析等需要全面了解的情况。',
      tips: '需要较长的解读时间，建议在安静的环境中进行，仔细分析每个位置的含义。'
    }
  ];

  const filteredCards = majorArcana.filter(card => 
    (selectedCategory === 'all' || selectedCategory === 'major_arcana') &&
    (searchTerm === '' || card.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
     card.keywords.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <>
      <Head>
        <title>学习塔罗奥秘 - 神秘塔罗牌占卜师</title>
        <meta name="description" content="深入学习塔罗牌知识，探索78张牌的含义和各种牌阵布局" />
      </Head>

      <main className="min-h-screen py-8">
        <div className="container-custom">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <Link href="/">
              <motion.button 
                whileHover={{ scale: 1.05, x: -5 }}
                className="btn-secondary flex items-center gap-2"
              >
                <ArrowLeft size={20} />
                返回首页
              </motion.button>
            </Link>
          </div>

          {/* Page Title */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-16"
          >
            <h1 className="text-responsive-xl font-mystical font-bold mb-6 text-gradient">
              塔罗奥秘学习
            </h1>
            <div className="mystical-divider max-w-32 mx-auto mb-6"></div>
            <p className="text-responsive-base text-gray-300 max-w-3xl mx-auto">
              深入了解塔罗牌的神秘世界，掌握78张牌的含义和解读艺术
            </p>
          </motion.div>

          {/* CardLibrary Section */}
          <section className="mb-20">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="mb-12"
            >
              <h2 className="text-responsive-lg font-mystical font-bold mb-6 text-white text-center">
                塔罗牌库
              </h2>
              
              {/* Search and Filter */}
              <div className="max-w-2xl mx-auto mb-8">
                <div className="relative mb-6">
                  <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    type="text"
                    placeholder="搜索塔罗牌..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="mystical-input pl-12"
                  />
                </div>
                
                <div className="flex justify-center gap-4">
                  {[
                    { id: 'all', label: '全部' },
                    { id: 'major_arcana', label: '大阿卡纳' },
                    { id: 'minor_arcana', label: '小阿卡纳' }
                  ].map((category) => (
                    <button
                      key={category.id}
                      onClick={() => setSelectedCategory(category.id as any)}
                      className={`px-6 py-2 rounded-xl font-semibold transition-all ${
                        selectedCategory === category.id
                          ? 'bg-gradient-to-r from-purple-500 to-blue-600 text-white'
                          : 'bg-gray-800/50 text-gray-300 hover:bg-gray-700/50'
                      }`}
                    >
                      {category.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Major Arcana Cards */}
              {(selectedCategory === 'all' || selectedCategory === 'major_arcana') && (
                <div className="mb-8">
                  <h3 className="text-xl font-mystical font-bold mb-6 text-purple-300 text-center">大阿卡纳</h3>
                  <div className="grid-responsive">
                    {filteredCards.map((card, index) => (
                      <motion.div
                        key={card.id}
                        initial={{ opacity: 0, scale: 0.9 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true }}
                        transition={{ delay: index * 0.1 }}
                        whileHover={{ y: -5 }}
                        onClick={() => setSelectedCard(selectedCard === card.id ? null : card.id)}
                        className="card-info cursor-pointer"
                      >
                        <div className="text-center">
                          <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-purple-500 to-blue-600 rounded-full flex items-center justify-center">
                            <span className="text-2xl font-bold text-white">{card.number}</span>
                          </div>
                          
                          <h4 className="text-lg font-mystical font-bold mb-2 text-white">
                            {card.name}
                          </h4>
                          
                          <p className="text-sm text-amber-300 mb-3">
                            {card.keywords}
                          </p>
                          
                          {selectedCard === card.id && (
                            <motion.div
                              initial={{ opacity: 0, height: 0 }}
                              animate={{ opacity: 1, height: 'auto' }}
                              className="mt-4 pt-4 border-t border-purple-500/30"
                            >
                              <p className="text-sm text-gray-300 leading-relaxed">
                                {card.description}
                              </p>
                            </motion.div>
                          )}
                          
                          <div className="mt-3 text-xs text-purple-300">
                            {selectedCard === card.id ? '点击收起' : '点击查看详情'}
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}

              {/* Minor Arcana Overview */}
              {(selectedCategory === 'all' || selectedCategory === 'minor_arcana') && (
                <div>
                  <h3 className="text-xl font-mystical font-bold mb-6 text-purple-300 text-center">小阿卡纳</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {minorArcana.map((suit, index) => (
                      <motion.div
                        key={suit.suit}
                        initial={{ opacity: 0, scale: 0.9 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true }}
                        transition={{ delay: index * 0.1 }}
                        whileHover={{ y: -5 }}
                        className="card-info text-center"
                      >
                        <div className={`w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center bg-gray-800/50`}>
                          <suit.icon className={`w-8 h-8 ${suit.color}`} />
                        </div>
                        
                        <h4 className="text-lg font-mystical font-bold mb-2 text-white">
                          {suit.name}
                        </h4>
                        
                        <p className="text-sm text-gray-300 leading-relaxed">
                          {suit.description}
                        </p>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          </section>

          {/* SpreadGuide Section */}
          <section>
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="mb-12"
            >
              <h2 className="text-responsive-lg font-mystical font-bold mb-6 text-white text-center">
                牌阵指南
              </h2>
              <div className="mystical-divider max-w-24 mx-auto mb-8"></div>
              <p className="text-gray-300 text-center max-w-3xl mx-auto mb-12">
                了解不同牌阵的用途和解读方法，选择最适合您问题的占卜方式
              </p>
              
              <div className="space-y-8">
                {spreadGuides.map((spread, index) => (
                  <motion.div
                    key={spread.id}
                    initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.2 }}
                    className="reading-card"
                  >
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                      {/* Spread Info */}
                      <div className="lg:col-span-1">
                        <div className="flex items-center gap-4 mb-4">
                          <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-600 rounded-full flex items-center justify-center">
                            <spread.icon className="w-6 h-6 text-white" />
                          </div>
                          <div>
                            <h3 className="text-xl font-mystical font-bold text-white">
                              {spread.name}
                            </h3>
                            <p className="text-sm text-gray-400">
                              {spread.cards} 张牌 • {spread.difficulty}
                            </p>
                          </div>
                        </div>
                        
                        <p className="text-gray-300 mb-4 leading-relaxed">
                          {spread.description}
                        </p>
                        
                        <div className="text-center p-4 bg-purple-900/30 rounded-xl border border-purple-500/30 mb-4">
                          <p className="text-amber-300 font-mono text-lg">
                            {spread.layout}
                          </p>
                          <p className="text-xs text-gray-400 mt-1">牌阵布局</p>
                        </div>
                      </div>

                      {/* Positions */}
                      <div className="lg:col-span-2">
                        <h4 className="text-lg font-mystical font-bold text-white mb-4">
                          牌位含义
                        </h4>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                          {spread.positions.map((position, posIndex) => (
                            <div key={posIndex} className="bg-gray-800/30 p-4 rounded-lg border border-gray-700/50">
                              <h5 className="font-semibold text-purple-300 mb-2">
                                {posIndex + 1}. {position.name}
                              </h5>
                              <p className="text-sm text-gray-300">
                                {position.description}
                              </p>
                            </div>
                          ))}
                        </div>
                        
                        <div className="space-y-3">
                          <div>
                            <h5 className="font-semibold text-amber-300 mb-1">适用场景</h5>
                            <p className="text-sm text-gray-300">{spread.usage}</p>
                          </div>
                          <div>
                            <h5 className="font-semibold text-amber-300 mb-1">占卜技巧</h5>
                            <p className="text-sm text-gray-300">{spread.tips}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </section>

          {/* Practice CTA */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mt-20"
          >
            <div className="reading-card">
              <h2 className="text-responsive-lg font-mystical font-bold mb-6 text-gradient">
                开始实践您的塔罗技艺
              </h2>
              
              <p className="text-gray-300 mb-8 leading-relaxed max-w-2xl mx-auto">
                学而时习之，不亦说乎。理论与实践相结合，才能真正掌握塔罗的奥秘
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/reading">
                  <motion.button
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    className="btn-primary flex items-center gap-3"
                  >
                    <BookOpen className="w-5 h-5" />
                    立即开始占卜
                  </motion.button>
                </Link>
                
                <Link href="/">
                  <motion.button
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    className="btn-secondary flex items-center gap-3"
                  >
                    <ArrowLeft className="w-5 h-5" />
                    返回首页
                  </motion.button>
                </Link>
              </div>
            </div>
          </motion.div>
        </div>
      </main>
    </>
  );
};

export default LearnPage;