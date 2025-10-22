
            -- Ensure tracking_events table has all required columns
            ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS email_captured VARCHAR(255);
            ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS country VARCHAR(100);
            ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS region VARCHAR(100);
            ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS city VARCHAR(100);
            ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS latitude DECIMAL(10, 8);
            ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS longitude DECIMAL(11, 8);
            ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'open';
            ALTER TABLE tracking_events ADD COLUMN IF NOT EXISTS landing_page_reached BOOLEAN DEFAULT FALSE;
            
            -- Ensure proper indexes for performance
            CREATE INDEX IF NOT EXISTS idx_tracking_events_timestamp ON tracking_events(timestamp);
            CREATE INDEX IF NOT EXISTS idx_tracking_events_link_id ON tracking_events(link_id);
            CREATE INDEX IF NOT EXISTS idx_tracking_events_status ON tracking_events(status);
            
            -- Fix notifications table for real-time timestamps
            ALTER TABLE notifications ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            ALTER TABLE notifications ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            
            -- Ensure campaigns table connects properly with links
            ALTER TABLE links ADD COLUMN IF NOT EXISTS campaign_name VARCHAR(255);
            ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS total_clicks INTEGER DEFAULT 0;
            ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS unique_visitors INTEGER DEFAULT 0;
            