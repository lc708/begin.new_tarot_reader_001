// frontend/src/lib/api.ts
/**
 * 前端API服务模块
 * 处理与后端MACore系统的所有通信
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 
  (process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8011/api');

// API响应类型定义
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface Card {
  name: string;
  reversed: boolean;
  position: number;
  orientation: string;
}

export interface ReadingResult {
  success: boolean;
  question?: string;
  question_category?: string;
  spread_type?: string;
  spread_name?: string;
  drawn_cards?: Card[];
  individual_readings?: any[];
  combined_reading?: string;
  reading_summary?: string;
  timestamp?: string;
  error?: string;  // 添加错误信息字段
}

export interface SpreadInfo {
  id: string;
  name: string;
  description: string;
  card_count: number;
  difficulty: string;
  usage: string;
}

export interface ReadingHistory {
  id: string;
  timestamp: string;
  user_question: string;
  question_category: string;
  spread_type: string;
  reading_summary: string;
}

export interface Statistics {
  total_readings: number;
  question_types: Record<string, number>;
  spread_types: Record<string, number>;
  most_recent: string;
  oldest: string;
  average_per_month: number;
}

// API请求函数
class TarotAPI {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const config = { ...defaultOptions, ...options };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // 健康检查
  async healthCheck(): Promise<ApiResponse> {
    return this.request('/health');
  }

  // 创建占卜
  async createReading(params: {
    question: string;
    spread_type?: string;
    save_result?: boolean;
  }): Promise<ReadingResult> {
    return this.request('/reading', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  // 获取牌阵列表
  async getSpreads(): Promise<ApiResponse<SpreadInfo[]>> {
    const response = await this.request<{ success: boolean; spreads: SpreadInfo[] }>('/spreads');
    return {
      success: response.success,
      data: response.spreads,
    };
  }

  // 获取特定牌阵详情
  async getSpreadDetail(spreadId: string): Promise<ApiResponse> {
    return this.request(`/spreads/${spreadId}`);
  }

  // 获取塔罗牌信息
  async getCards(searchTerm?: string): Promise<ApiResponse<string[]>> {
    const query = searchTerm ? `?search=${encodeURIComponent(searchTerm)}` : '';
    const response = await this.request<{ success: boolean; cards: string[]; total: number }>(`/cards${query}`);
    return {
      success: response.success,
      data: response.cards,
    };
  }

  // 获取占卜历史
  async getReadingHistory(params: {
    limit?: number;
    offset?: number;
  } = {}): Promise<ApiResponse<{
    readings: ReadingHistory[];
    total: number;
    limit: number;
    offset: number;
  }>> {
    const query = new URLSearchParams();
    if (params.limit) query.append('limit', params.limit.toString());
    if (params.offset) query.append('offset', params.offset.toString());
    
    const queryString = query.toString();
    const endpoint = `/history${queryString ? `?${queryString}` : ''}`;
    
    const response = await this.request<{
      success: boolean;
      readings: ReadingHistory[];
      total: number;
      limit: number;
      offset: number;
    }>(endpoint);
    
    return {
      success: response.success,
      data: {
        readings: response.readings,
        total: response.total,
        limit: response.limit,
        offset: response.offset,
      },
    };
  }

  // 获取统计信息
  async getStatistics(): Promise<ApiResponse<Statistics>> {
    const response = await this.request<{ success: boolean; statistics: Statistics }>('/statistics');
    return {
      success: response.success,
      data: response.statistics,
    };
  }

  // 推荐牌阵
  async recommendSpread(question: string): Promise<ApiResponse<{
    recommended_spread: string;
    spread_info: any;
    reason: string;
  }>> {
    return this.request('/recommend-spread', {
      method: 'POST',
      body: JSON.stringify({ question }),
    });
  }
}

// 创建API实例
export const tarotAPI = new TarotAPI();

// React Hook for API calls with error handling
export function useAPI() {
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const callAPI = async <T>(apiCall: () => Promise<T>): Promise<T | null> => {
    setLoading(true);
    setError(null);

    try {
      const result = await apiCall();
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setError(errorMessage);
      console.error('API call failed:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { loading, error, callAPI };
}

// 导入React用于hook
import React from 'react';
