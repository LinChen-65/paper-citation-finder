import React, { useState } from 'react';
import { Layout, Input, Button, Card, List, Spin, Typography, Tabs } from 'antd';
import axios from 'axios';
import './App.css';

const { Header, Content } = Layout;
const { Search } = Input;
const { Title, Text } = Typography;
const { TabPane } = Tabs;

function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = async (value) => {
    if (!value.trim()) return;
    
    setLoading(true);
    setSearchQuery(value);
    
    try {
      const response = await axios.post('/api/search', { query: value });
      setResults(response.data);
    } catch (error) {
      console.error('Search error:', error);
      // Handle error appropriately
    } finally {
      setLoading(false);
    }
  };

  const renderCitationItem = (item, index) => (
    <List.Item key={index}>
      <Card size="small">
        <Text strong>{item.title}</Text>
        <br />
        <Text type="secondary">{item.source}</Text>
        <br />
        <Text>{item.snippet}</Text>
      </Card>
    </List.Item>
  );

  return (
    <Layout className="layout">
      <Header className="header">
        <Title level={2} style={{ color: 'white', margin: 0 }}>
          论文引用检索系统
        </Title>
      </Header>
      <Content className="content">
        <div className="search-container">
          <Search
            placeholder="输入论文DOI、标题或粘贴论文信息"
            allowClear
            enterButton="搜索引用"
            size="large"
            onSearch={handleSearch}
            loading={loading}
            disabled={loading}
          />
        </div>
        
        {loading && (
          <div className="loading-container">
            <Spin size="large" tip="正在搜索引用..." />
          </div>
        )}
        
        {results && !loading && (
          <div className="results-container">
            <Tabs defaultActiveKey="1">
              <TabPane tab={`学术论文 (${results.academic?.length || 0})`} key="1">
                {results.academic?.length > 0 ? (
                  <List
                    itemLayout="vertical"
                    dataSource={results.academic}
                    renderItem={renderCitationItem}
                  />
                ) : (
                  <Text>未找到相关学术论文引用</Text>
                )}
              </TabPane>
              
              <TabPane tab={`国际课件 (${results.slides_international?.length || 0})`} key="2">
                {results.slides_international?.length > 0 ? (
                  <List
                    itemLayout="vertical"
                    dataSource={results.slides_international}
                    renderItem={renderCitationItem}
                  />
                ) : (
                  <Text>未找到相关国际课件</Text>
                )}
              </TabPane>
              
              <TabPane tab={`中文资源 (${results.chinese?.length || 0})`} key="3">
                {results.chinese?.length > 0 ? (
                  <List
                    itemLayout="vertical"
                    dataSource={results.chinese}
                    renderItem={renderCitationItem}
                  />
                ) : (
                  <Text>未找到相关中文资源</Text>
                )}
              </TabPane>
            </Tabs>
          </div>
        )}
      </Content>
    </Layout>
  );
}

export default App;