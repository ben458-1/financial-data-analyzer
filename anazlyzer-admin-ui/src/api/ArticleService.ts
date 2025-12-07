import { getRequest } from './LoginService';
import { ArticleContentConfigResponse } from '../components/article-configuration/article-content/ArticleContentConfiguration';
import { Newspaper } from '../components/pages/configuration/Article';
import { message } from 'antd';
import { ArticleMetaConfigProp } from '../components/article-configuration/article-metadata/ArticleMetadataConfiguration';

export const fetchNewspapers = async (): Promise<Newspaper[] | null> => {
    try {
        const data = await getRequest<Newspaper[]>('/articles/v1/news');

        if (Array.isArray(data)) {
            return data;
        } else {
            console.error('Unexpected response format:', data);
            message.error('Unexpected response format');
            return null;
        }
    } catch (error) {
        console.error('Error fetching articles:', error);
        message.error('Error fetching articles');
        return null;
    }
};


export const fetchArticleMetaConfig = async (
    newspaperId: number
): Promise<Map<string, ArticleMetaConfigProp[]> | null> => {
    try {
        const rawData = await getRequest<Record<string, ArticleMetaConfigProp[]>>(
            `/articles/v1/config/article-meta/${newspaperId}`
        );

        if (!rawData || Object.keys(rawData).length === 0) {
            console.warn(`No meta config found for newspaperId: ${newspaperId}`);
            return null;
        }

        return new Map<string, ArticleMetaConfigProp[]>(Object.entries(rawData));
    } catch (error) {
        console.error(`Error fetching article meta config for newspaperId ${newspaperId}:`, error);
        throw new Error('Failed to fetch article meta configuration');
    }
};


export const fetchArticleContentConfig = async (
    newspaperId: number
): Promise<ArticleContentConfigResponse | null> => {
    try {
        const data = await getRequest<ArticleContentConfigResponse>(
            `/articles/v1/config/article-content/${newspaperId}`
        );

        if (!data?.doc) {
            console.error(`No document found for newspaperId: ${newspaperId}`);
            return null;
        }

        if (data?.doc?.newspaperID === newspaperId) {
            return data;
        }

        console.error(`Mismatch in newspaperId: Expected ${newspaperId}, got ${data?.doc?.newspaperID}`);
        return null;
    } catch (error) {
        console.error('Error fetching article config:', error);
        throw new Error('Failed to fetch article configuration');
    }
};

