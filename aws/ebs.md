# Amazon EBS 儲存格式比較

Amazon EBS（Elastic Block Store）提供多種儲存格式，以滿足不同工作負載的需求。

## EBS 磁碟區類型比較

| 磁碟區類型 | 用途 | 特點 |
|---|---|---|
| 通用型 SSD (gp2/gp3) | 適用於多數交易工作負載，提供價格與效能的平衡。 | 提供穩定的基準效能，並可短時間爆發至更高 IOPS。gp3 相較 gp2，使用者可依自身需求去調整IOPS與輸送量的效能。 |
| 佈建 IOPS SSD (io1/io2) | 適用於需要高 IOPS 和低延遲的 I/O 密集型工作負載，例如資料庫。 | 提供可預測的效能，使用者可自行佈建所需的 IOPS。io2 磁碟區提供更高的 IOPS/GB 比例和更高的耐用性。 |
| 輸送量最佳化 HDD (st1) | 適用於頻繁存取、輸送量密集型的工作負載，例如大數據、資料倉儲。 | 提供高輸送量，但 IOPS 較低。 |
| 冷 HDD (sc1) | 適用於不常存取的冷資料，例如檔案儲存。 | 成本最低，但輸送量和 IOPS 也最低。 |

## EBS 的重要考量因素

* **效能 (IOPS 和輸送量)：**
    * 根據工作負載的需求選擇適當的效能層級。
* **成本：**
    * 不同類型的 EBS 磁碟區有不同的定價，應根據預算選擇。
* **耐用性：**
    * EBS 磁碟區提供高耐用性，但建議定期備份重要資料。
* **工作負載類型：**
    * 交易型工作負載通常需要高 IOPS，而輸送量密集型工作負載則需要高輸送量。

## EBS 與其他 AWS 儲存服務的比較

* **EBS vs. EFS (Elastic File System)：**
    * EBS 是區塊層級儲存，適用於 EC2 執行個體。
    * EFS 是檔案層級儲存，可供多個 EC2 執行個體同時存取。
* **EBS vs. S3 (Simple Storage Service)：**
    * EBS 是區塊層級儲存，適用於 EC2 執行個體。
    * S3 是物件層級儲存，適用於儲存和檢索大量資料。

## 重點摘要

* EBS 提供多種儲存類型，以滿足不同效能和成本需求。
* 根據工作負載的特性選擇適當的 EBS 磁碟區類型。
* 了解EBS與AWS其他儲存服務之間的差異，以便為您的應用程式選擇最佳的儲存解決方案。