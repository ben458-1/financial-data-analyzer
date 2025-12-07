import React from 'react';
import { Card, Typography, Button, Image } from 'antd';

const { Title, Paragraph, Text } = Typography;

interface ArticleProps {
    article: {
        source: string;
        sector: string;
        Headline: string;
        Author: string;
        Date: string;
        preamble: string;
        image: string;
        body: string;
    };
    onBack: () => void;
}

const Article: React.FC<ArticleProps> = ({ article, onBack }) => {
    return (
        <Card
            style={{ maxWidth: 1500, margin: '0 auto', padding: 24, borderRadius: 16 }}
            bodyStyle={{ padding: 24 }}
        >
            <Button type="link" onClick={onBack} style={{ marginBottom: 16 }}>
                ← Back to Articles
            </Button>
            <Title level={2}>{article.Headline}</Title>
            <Paragraph type="secondary">
                <Text strong>{article.Author}</Text> · {article.Date} · <Text italic>{article.source}</Text>
            </Paragraph>
            <div style={{ textAlign: 'center' }}>
                <Image
                    src={article.image}
                    alt="article"
                    style={{
                        width: '100%',
                        maxHeight: '400px',
                        objectFit: 'cover',
                        borderRadius: 12,
                        marginBottom: 24,
                    }}
                />
            </div>
            <Paragraph>{article.preamble}</Paragraph>
            <Paragraph><pre
                style={{
                    background: '#f8f9fa',
                    padding: '24px',
                    borderRadius: '12px',
                    fontSize: '16px',
                    lineHeight: '1.8',
                    fontFamily: 'Segoe UI, Roboto, sans-serif',
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                    color: '#2c3e50',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
                    marginBottom: 0,
                }}
            >{article.body}</pre></Paragraph>
        </Card>
    );
};

export default Article;
