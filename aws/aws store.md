# AWS 儲存服務重點整理與比較

AWS 提供多樣化的儲存服務，以滿足不同應用場景的需求。以下是各服務的重點整理與比較：

## 1. Amazon S3 (Simple Storage Service)

* **特性：**
    * 物件儲存服務，適用於各種資料類型。
    * 提供高擴展性、資料可用性、安全性和效能。
    * 提供多種儲存類別，以優化成本和存取模式。
* **應用場景：**
    * 靜態網站託管、資料備份和還原、媒體儲存、大數據分析、**資料湖和伺服器無伺服器查詢**。
* **重點功能：**
    * 版本控制、跨區域複寫 (CRR)、生命週期管理、物件鎖定。
* **衍伸服務與重要概念：**
    * **S3 Transfer Acceleration：** 利用 AWS 全球加速網路，加速資料傳輸到 S3。
    * **S3 Intelligent-Tiering：** 自動在不同存取層之間移動資料，以優化成本。
    * **S3 Glacier Instant Retrieval：** 低成本的長期儲存，具有毫秒級的存取速度。
    * **S3 Access Points：** 管理大規模 S3 資料存取的具名網路端點，簡化跨多個應用程式的存取控制。
    * **S3 Object Lambda：** 在從 S3 檢索資料時，添加自己的程式碼以修改和處理資料。
    * **S3 Event Notifications：** 在 S3 儲存桶中發生特定事件時觸發通知 (例如，物件建立、刪除)。可與 SNS、SQS 和 Lambda 等服務集成。
    * **AWS DataSync：** 安全且高效地在內部部署儲存系統與 Amazon S3 之間傳輸資料。
    * **AWS Storage Lens：** 提供組織範圍的物件儲存可見性，識別成本優化機會和應用最佳實踐。
    * **S3 Select：** 使用 SQL 表達式直接從 S3 物件中檢索部分資料，減少資料傳輸和處理成本。
    * **Amazon Athena：** 無伺服器互動式查詢服務，可使用標準 SQL 直接分析 S3 中的資料。
* **SAA 考試重點:**
    * 儲存類別的選擇與使用時機。
    * 儲存桶政策(Bucket policy)與ACL的差異，IAM的存取控制。
    * S3 Transfer Acceleration與多段上傳的效能優化。
    * 伺服器端與客戶端加密。
    * 成本優化的生命週期政策與S3 intelligent-Tiering。
    * **S3 事件通知的使用場景。**
    * **S3 Access Points 的優勢。**
    * **S3 Select 的使用案例和優勢。**
    * **Amazon Athena 的使用案例和工作原理。**

## 2. Amazon EBS (Elastic Block Store)

* **特性：**
    * 區塊層級儲存，適用於 EC2 執行個體。
    * 提供多種磁碟區類型，以滿足不同效能和成本需求。
* **應用場景：**
    * 作業系統磁碟、資料庫、應用程式儲存。
* **磁碟區類型：**
    * 通用型 SSD (gp2/gp3)、佈建 IOPS SSD (io1/io2)、輸送量最佳化 HDD (st1)、冷 HDD (sc1)。
* **重要考量因素：**
    * 效能 (IOPS 和輸送量)、成本、耐用性、工作負載類型。
* **衍伸服務與重要概念：**
    * **EBS 快照 (Snapshot)：** 磁碟區的時間點副本，可用於備份和建立新磁碟區。
    * **EBS 快照生命週期管理員 (DLM)：** 自動化 EBS 快照的建立、保留和刪除。
* **SAA 考試重點:**
    * 各種EBS磁碟的效能與價格差異。
    * EBS快照(snapshot)的應用與限制。
    * EBS加密。
    * **EBS 快照生命週期管理員 (DLM) 的用途。**

## 3. Amazon EFS (Elastic File System)

* **特性：**
    * 可擴展的彈性檔案系統，適用於 Linux 型 EC2 執行個體。
    * 支援多個 EC2 執行個體同時存取相同的檔案系統。
    * 適用於需要共享檔案存取的工作負載。
* **應用場景：**
    * Web 伺服器和內容管理系統、開發環境和程式碼儲存庫、大數據分析和機器學習、媒體處理工作流程。
* **衍伸服務與重要概念：**
    * **EFS One Zone：** 一個可用區域中的檔案系統，成本較低，但可用性較低。
    * **EFS 傳輸加速器 (EFS Transfer Acceleration)：** 使用 AWS 全球網路加速 EFS 的檔案傳輸。
    * **EFS 生命週期管理：** 自動將不常存取的檔案移動到成本更低的儲存層。

## 4. Amazon FSx

* **特性：**
    * 全受管的檔案系統，支援 Windows File Server 和 Lustre 等熱門檔案系統。
    * 針對特定工作負載進行優化，提供高效能和豐富的功能。
* **應用場景：**
    * Windows 型應用程式和企業應用程式、高效能運算 (HPC) 和機器學習、影片編輯和媒體轉碼。
* **衍伸服務與重要概念：**
    * **FSx for Windows File Server 的 Active Directory 集成。**
    * **FSx for Lustre 的並行檔案存取和高效能特性。**

## 5. Amazon Glacier 和 Amazon Glacier Deep Archive

* **特性：**
    * 低成本的長期封存儲存。
    * 適用於不常存取的資料，例如備份和合規性資料。
    * Glacier Deep Archive 為更低成本的選擇。
* **應用場景：**
    * 長期備份和災難復原、數位媒體封存、合規性資料儲存。
* **衍伸服務與重要概念：**
    * **Glacier Instant Retrieval 的快速存取特性。**
    * **Glacier Flexible Retrieval 和 Glacier Deep Archive 的不同檢索時間和成本。**
    * **Vault Lock：** 允許您實施合規性控制，以限制 Glacier Vault 的存取。

## 6. AWS Storage Gateway

* **特性：**
    * 將內部部署應用程式連接到 AWS 雲端儲存。
    * 提供檔案閘道、磁帶閘道和磁碟區閘道等多種閘道類型。
    * 混合雲環境的理想選擇。
* **應用場景：**
    * 混合雲備份和災難復原。
    * 將內部部署資料移轉到 AWS。
    * 擴充內部部署儲存容量。
* **衍伸服務與重要概念：**
    * **檔案閘道 (File Gateway)：** 提供 NFS 和 SMB 介面，用於存取 S3 中的物件。
    * **磁帶閘道 (Tape Gateway)：** 提供虛擬磁帶櫃 (VTL) 介面，用於備份應用程式。
    * **磁碟區閘道 (Volume Gateway)：** 提供 iSCSI 介面，用於區塊層級的儲存備份和災難復原。

## 7. AWS Backup

* **特性：**
    * 集中管理跨 AWS 服務的備份。
    * 支援 EC2、EBS、RDS、DynamoDB 和 EFS 等多種服務。
    * 簡化備份和還原程序。
* **應用場景：**
    * 集中化備份管理。
    * 合規性和稽核。
    * 災難復原。
* **衍伸服務與重要概念：**
    * **Backup Plans：** 定義備份頻率、保留策略和目標儲存庫。
    * **Backup Vaults：** 安全地儲存備份的容器。
    * **Cross-Region Backup：** 將備份複製到不同的 AWS 區域以實現災難復原。

## AWS 儲存服務比較表

| 服務名稱 | 儲存類型 | 主要應用場景 | 優點 | SAA 考試重點 | 適用服務 | **衍伸服務/重要概念** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Amazon S3 | 物件儲存 | 網站託管、備份、資料湖、**伺服器無伺服器查詢** | 高可擴展性、耐用性、成本效益、**直接 SQL 查詢能力** | 儲存類別選擇,存取控制,效能優化,加密,成本優化 | S3 | Transfer Acceleration, Intelligent-Tiering, Glacier Instant Retrieval, Access Points, Object Lambda, Event Notifications, DataSync, Storage Lens, **S3 Select, Amazon Athena** |
| Amazon EBS | 區塊儲存 | EC2 執行個體儲存、資料庫 | 高效能、低延遲、可調整大小 | 磁碟類型,快照(snapshot),加密 | EC2 | 快照 (Snapshot), 快照生命週期管理員 (DLM) |
| Amazon EFS | 檔案儲存 | 共享檔案系統、Web 應用程式 | 彈性擴展、多個 EC2 存取 | / | EC2 | One Zone, 傳輸加速器, 生命週期管理 |
| Amazon FSx | 檔案儲存 | Windows 應用程式、高效能運算 | 高效能、與 Windows 相容 | / | EC2 | Active Directory 集成 (Windows), 並行存取 (Lustre) |
| Amazon Glacier / Deep Archive | 封存儲存 | 長期備份、合規性 | 極低成本、長期儲存 | / | S3 | Instant Retrieval, Flexible Retrieval, Deep Archive, Vault Lock |
| AWS Storage Gateway | 混合雲儲存 | 混合雲備份、內部部署整合 | 內部部署整合、雲端擴充 | / | EC2,S3,Glacier | 檔案閘道, 磁帶閘道, 磁碟區閘道 |
| AWS Backup | 備份管理 | 集中備份、跨服務備份 | 集中管理、簡化備份 | / | EC2,EBS,RDS,DynamoDB,EFS | Backup Plans, Backup Vaults, Cross-Region Backup |
